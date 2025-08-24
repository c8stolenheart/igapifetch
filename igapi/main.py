from flask import Flask, request, jsonify
import instaloader
from urllib.parse import urlparse
import os

# Flask app
app = Flask(__name__)

# Set your Instagram sessionid here
SESSIONID = "59056190733%3AMu11iOstt79Stp%3A12%3AAYdQoHbNqf8cqvHLgO2Wd5FpaJ2MsPCe5GnIh8mVPw"  # <-- Replace this

# Setup Instaloader with session
L = instaloader.Instaloader()
L.context._session.cookies.set("sessionid", SESSIONID)

# Output files
profile_output = "profile.txt"
post_output = "post.txt"

def extract_username_from_url(url):
    try:
        path = urlparse(url).path.strip("/")
        username = path.split("/")[0]
        return username
    except:
        return None

def is_post_url(url):
    return any(x in url for x in ["/p/", "/reel/", "/tv/"])

def get_username_stats(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        data = {
            "username": username,
            "followers": profile.followers
        }
        with open(profile_output, "a", encoding="utf-8") as f:
            f.write(f"Username:{username}|Startcount:{profile.followers}\n")
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_post_stats(post_url):
    try:
        shortcode = urlparse(post_url).path.strip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        data = {
            "url": post_url,
            "likes": post.likes
        }
        with open(post_output, "a", encoding="utf-8") as f:
            f.write(f"{post_url}|Start count:{post.likes}\n")
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# API endpoints
@app.route("/profile", methods=["GET"])
def profile_api():
    username_or_url = request.args.get("user")
    if not username_or_url:
        return jsonify({"status": "error", "message": "Missing ?user="}), 400

    username = extract_username_from_url(username_or_url) if "http" in username_or_url else username_or_url
    return jsonify(get_username_stats(username))

@app.route("/post", methods=["GET"])
def post_api():
    post_url = request.args.get("url")
    if not post_url:
        return jsonify({"status": "error", "message": "Missing ?url="}), 400

    return jsonify(get_post_stats(post_url))

if __name__ == "__main__":
    # Run API on all network interfaces (important for VPS)
    app.run(host="0.0.0.0", port=5000)


