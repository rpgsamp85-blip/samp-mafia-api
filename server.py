import os
from flask import Flask, request, jsonify

app = Flask(__name__)

game_state = {
    "active": False,
    "phase": "none",
    "players": {}
}

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(game_state)

@app.route('/update', methods=['POST'])
def update_state():
    global game_state
    data = request.json
    if data:
        game_state = data
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/vote', methods=['POST'])
def register_vote():
    data = request.json
    target_id = str(data.get("target_id"))
    
    if target_id in game_state["players"]:
        game_state["players"][target_id]["votes"] += 1
        return jsonify({"status": "success", "players": game_state["players"]})
    
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
