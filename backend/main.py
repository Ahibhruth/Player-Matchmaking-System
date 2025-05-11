from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend access

# Sample player data stored in a dictionary
players = {
    "Alice": {"rank": 10, "playstyle": "aggressive"},
    "Bob": {"rank": 12, "playstyle": "defensive"},
    "Charlie": {"rank": 15, "playstyle": "balanced"},
    "Daisy": {"rank": 11, "playstyle": "aggressive"},
    "Eve": {"rank": 13, "playstyle": "defensive"},
    "Frank": {"rank": 10, "playstyle": "balanced"},
    "Grace": {"rank": 12, "playstyle": "aggressive"},
    "Hank": {"rank": 9, "playstyle": "defensive"},
    "Ivy": {"rank": 15, "playstyle": "balanced"},
    "Jake": {"rank": 14, "playstyle": "aggressive"},
    "Kara": {"rank": 16, "playstyle": "defensive"},
    "Leo": {"rank": 17, "playstyle": "balanced"},
    "Mia": {"rank": 18, "playstyle": "aggressive"},
    "Nate": {"rank": 10, "playstyle": "defensive"},
    "Olive": {"rank": 13, "playstyle": "balanced"},
    "Paul": {"rank": 11, "playstyle": "aggressive"},
    "Quinn": {"rank": 12, "playstyle": "defensive"},
    "Rose": {"rank": 15, "playstyle": "balanced"},
    "Steve": {"rank": 16, "playstyle": "aggressive"},
    "Tina": {"rank": 17, "playstyle": "defensive"},
    "Uma": {"rank": 14, "playstyle": "balanced"},
    "Victor": {"rank": 13, "playstyle": "aggressive"},
    "Wendy": {"rank": 12, "playstyle": "defensive"},
    "Xander": {"rank": 15, "playstyle": "balanced"},
    "Yara": {"rank": 11, "playstyle": "aggressive"},
    "Zack": {"rank": 10, "playstyle": "defensive"},
    "Aria": {"rank": 19, "playstyle": "balanced"},
    "Blake": {"rank": 20, "playstyle": "aggressive"},
    "Cora": {"rank": 9, "playstyle": "defensive"},
    "Drew": {"rank": 8, "playstyle": "balanced"},
    "Elle": {"rank": 14, "playstyle": "aggressive"},
    "Finn": {"rank": 13, "playstyle": "defensive"},
    "Gia": {"rank": 16, "playstyle": "balanced"},
    "Hugo": {"rank": 17, "playstyle": "aggressive"},
    "Iris": {"rank": 18, "playstyle": "defensive"},
    "Jude": {"rank": 12, "playstyle": "balanced"},
    "Kris": {"rank": 14, "playstyle": "aggressive"},
    "Lara": {"rank": 15, "playstyle": "defensive"},
    "Milo": {"rank": 10, "playstyle": "balanced"},
    "Nora": {"rank": 11, "playstyle": "aggressive"},
    "Omar": {"rank": 12, "playstyle": "defensive"},
    "Pia": {"rank": 13, "playstyle": "balanced"},
    "Rex": {"rank": 14, "playstyle": "aggressive"},
    "Sara": {"rank": 15, "playstyle": "defensive"},
    "Toby": {"rank": 16, "playstyle": "balanced"},
    "Usha": {"rank": 17, "playstyle": "aggressive"},
    "Vik": {"rank": 18, "playstyle": "defensive"},
    "Will": {"rank": 19, "playstyle": "balanced"},
    "Zoe": {"rank": 20, "playstyle": "aggressive"}
}

@app.route('/api/register_player', methods=['POST'])
def register_player():
    data = request.get_json()
    name = data.get('name')
    rank = data.get('rank')
    playstyle = data.get('playstyle')

    if name not in players:
        players[name] = {'rank': rank, 'playstyle': playstyle}
        return jsonify({"message": "Player registered successfully!"}), 200
    else:
        return jsonify({"message": "Player already exists!"}), 400

@app.route('/match/<name>', methods=['GET'])
def match_player(name):
    if name not in players:
        return jsonify({"error": "Player not found!"}), 404

    player = players[name]
    matches = []

    for other_name, info in players.items():
        if other_name != name:
            if abs(player['rank'] - info['rank']) <= 5 and player['playstyle'] == info['playstyle']:
                matches.append(other_name)

    if matches:
        return jsonify({"matches": matches}), 200
    else:
        return jsonify({"error": "No matching players found!"}), 404

@app.route('/api/delete_player/<name>', methods=['DELETE'])
def delete_player(name):
    if name in players:
        del players[name]
        return jsonify({"message": f"Player {name} deleted successfully."}), 200
    else:
        return jsonify({"error": "Player not found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
