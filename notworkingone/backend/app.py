import time
import jwt
import requests
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from passlib.context import CryptContext

SECRET_KEY = "CHANGE_ME_SECRET"
JWT_ALGO = "HS256"
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo user
USER = {
    "username": "admin",
    "password_hash": pwd_ctx.hash("admin123")
}

# Friend's AI stream (example: MJPEG stream)
AI_STREAM_URL = "http://ai-flask:6000/stream"

app = Flask(__name__)
CORS(app)


# ---------- Auth ----------
@app.post("/login")
def login():
    data = request.json
    if not data:
        return {"error": "Missing credentials"}, 400

    if data["username"] != USER["username"] or not pwd_ctx.verify(data["password"], USER["password_hash"]):
        return {"error": "Invalid credentials"}, 401

    token = jwt.encode({"sub": data["username"], "iat": time.time()}, SECRET_KEY, algorithm=JWT_ALGO)
    return {"access_token": token}


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGO])
    except Exception:
        return None


# ---------- Proxy stream ----------
@app.get("/video")
def video():
    token = request.args.get("token")
    if not token or not verify_token(token):
        return {"error": "Unauthorized"}, 401

    r = requests.get(AI_STREAM_URL, stream=True)
    return Response(r.iter_content(chunk_size=1024),
                    content_type=r.headers.get("Content-Type", "multipart/x-mixed-replace; boundary=frame"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)