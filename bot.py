from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# In-memory database (change to real DB if needed)
banned_users = {}

@app.route('/')
def home():
    return "Ban System Online"

@app.route('/ban', methods=['POST'])
def ban_user():
    data = request.json
    user_id = str(data.get("userId"))
    username = data.get("username")

    banned_users[user_id] = username
    return jsonify({"message": f"{username} is now banned."})

@app.route('/checkban')
def check_ban():
    user_id = request.args.get("userid")
    banned = user_id in banned_users
    return jsonify({"banned": banned})

@app.route('/unban', methods=['POST'])
def unban_user():
    data = request.json
    user_id = str(data.get("userId"))

    if user_id in banned_users:
        del banned_users[user_id]
        return jsonify({"message": f"User {user_id} unbanned."})
    else:
        return jsonify({"message": "User not found."}), 404

@app.route('/interactions', methods=['POST'])
def interactions():
    data = request.json
    try:
        custom_id = data["data"]["custom_id"]
        if custom_id.startswith("unban_"):
            user_id = custom_id.split("_")[1]

            if user_id in banned_users:
                del banned_users[user_id]
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": f"✅ Unbanned user with ID: {user_id}"
                    }
                })
            else:
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": f"User {user_id} not found in ban list."
                    }
                })
        else:
            return jsonify({
                "type": 4,
                "data": {
                    "content": "Invalid button."
                }
            })
    except Exception as e:
        return jsonify({
            "type": 4,
            "data": {
                "content": f"Error: {str(e)}"
            }
        })

if __name__ == '__main__':
    app.run()
