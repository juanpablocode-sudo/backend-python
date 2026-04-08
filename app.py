from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def load_users():
    try:
        with open("users.json") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    return "API funcionando 🚀"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    users = load_users()

    username = data["username"]

    if username not in users:
        users[username] = {"points": 0}

    save_users(users)
    return jsonify(users[username])

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    users = load_users()

    users[data["username"]] = {
        "points": data["points"]
    }

    save_users(users)
    return jsonify({"ok": True})

@app.route("/ranking")
def ranking():
    users = load_users()
    sorted_users = sorted(users.items(), key=lambda x: x[1]["points"], reverse=True)
    return jsonify(sorted_users[:5])

app.run(host="0.0.0.0", port=10000)
