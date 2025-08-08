from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import json

app = Flask(__name__)

# Store bans
banned_users = {}  # key: userId, value: username

@app.route('/ban', methods=['POST'])
def ban_user():
    data = request.json
    user_id = str(data['userId'])
    username = data['username']
    banned_users[user_id] = username
    return jsonify({"status": "banned"}), 200

@app.route('/checkban', methods=['GET'])
def check_ban():
    user_id = request.args.get('userid')
    if user_id in banned_users:
        return jsonify({"banned": True})
    return jsonify({"banned": False})

@app.route('/', methods=['POST'])
def discord_interaction():
    data = request.json
    if data["type"] == 3:  # BUTTON click
        custom_id = data["data"]["custom_id"]
        if custom_id.startswith("unban_"):
            user_id = custom_id.split("_")[1]
            banned_users.pop(user_id, None)
            return jsonify({
                "type": 4,
                "data": {
                    "content": f"✅ Unbanned user ID `{user_id}`."
                }
            })
    return jsonify({"type": 5})  # ACK

if __name__ == "__main__":
    app.run(port=3000)
