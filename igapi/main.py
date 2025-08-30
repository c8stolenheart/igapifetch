from flask import Flask, request, jsonify
import instaloader
from urllib.parse import urlparse

app = Flask(__name__)

# -----------------------
# Instagram session setup
# -----------------------
SESSIONID = "59056190733%3Ae7z2oBuS07bk61%3A19%3AAYeeqXkZkFe8l4IOOubGVj-rjnLHg3AryGwi1oRWwQ"

L = instaloader.Instaloader()

cookies = {
    "sessionid": "59056190733%3Ae7z2oBuS07bk61%3A19%3AAYeeqXkZkFe8l4IOOubGVj-rjnLHg3AryGwi1oRWwQ",
    "csrftoken": "w75TMuhCfHtktZj0smxIJC6J5TyIiAya",
    "ds_user_id": "59056190733",
    "rur": "HIL,59056190733,1788118927:01fe61a8fcfad6365e5c658858a29e80c92a80e20834972b6bb27dc52fd2c879e89bf7a0",
    "mid": "ZuJ0dAALAAFwyT5NFDpui1lyGMaL",
    "ig_did": "36040C08-62F0-4CD9-9E8B-31DA9D2CDBD7",
    "datr": "w4oYZ9asKELkDJVWhgOuTihU",
    "ig_nrcb": "1"
}

for k, v in cookies.items():
    L.context._session.cookies.set(k, v, domain=".instagram.com")

# Output files
profile_output = "profile.txt"
post_output = "post.txt"

# -----------------------
# Helpers
# -----------------------
from flask import Flask, request, jsonify
import instaloader
from urllib.parse import urlparse

app = Flask(__name__)

# -----------------------
# Instagram session setup
# -----------------------
L = instaloader.Instaloader()

# ⚠️ Replace with fresh cookies from your browser when session expires
cookies = {
    "sessionid": "59056190733%3Ae7z2oBuS07bk61%3A19%3AAYeeqXkZkFe8l4IOOubGVj-rjnLHg3AryGwi1oRWwQ",
    "csrftoken": "w75TMuhCfHtktZj0smxIJC6J5TyIiAya",
    "ds_user_id": "59056190733",
    "rur": "HIL,59056190733,1788118927:01fe61a8fcfad6365e5c658858a29e80c92a80e20834972b6bb27dc52fd2c879e89bf7a0",
    "mid": "ZuJ0dAALAAFwyT5NFDpui1lyGMaL",
    "ig_did": "36040C08-62F0-4CD9-9E8B-31DA9D2CDBD7",
    "datr": "w4oYZ9asKELkDJVWhgOuTihU",
    "ig_nrcb": "1"
}

for k, v in cookies.items():
    L.context._session.cookies.set(k, v, domain=".instagram.com")

# Output log files
profile_output = "profile.txt"
post_output = "post.txt"

# -----------------------
# Helpers
# -----------------------
def extract_username_from_url(url):
    try:
        path = urlparse(url).path.strip("/")
        return path.split("/")[0]
    except Exception:
        return None

def get_username_stats(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        data = {
            "username": username,
            "followers": profile.followers
        }
        with open(profile_output, "a", encoding="utf-8") as f:
            f.write(f"Username:{username}|Followers:{profile.followers}\n")
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
            f.write(f"{post_url}|Likes:{post.likes}\n")
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -----------------------
# API Endpoints
# -----------------------
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

# -----------------------
# Run Flask app
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

