from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample player data stored in a dictionary
players = {}
players['Alice'] = {'rank': 10, 'playstyle': 'aggressive'}
players['Bob'] = {'rank': 12, 'playstyle': 'defensive'}
players['Charlie'] = {'rank': 15, 'playstyle': 'balanced'}

# Register a new player
@app.route('/api/register_player', methods=['POST'])
def register_player():
    data = request.get_json()
    player_name = data.get('name')
    player_rank = data.get('rank')
    player_playstyle = data.get('playstyle')

    # Add player to the dictionary
    if player_name not in players:
        players[player_name] = {'rank': player_rank, 'playstyle': player_playstyle}
        return jsonify({"message": "Player registered successfully!"}), 200
    else:
        return jsonify({"message": "Player already exists!"}), 400

# Find matching players based on name
@app.route('/match/<name>', methods=['GET'])
def match_player(name):
    if name not in players:
        return jsonify({"error": "Player not found!"}), 404

    player = players[name]
    possible_matches = []

    # Logic to find players close in rank and matching playstyles
    for other_name, info in players.items():
        if other_name != name:
            rank_diff = abs(player['rank'] - info['rank'])
            playstyle_match = player['playstyle'] == info['playstyle']

            if rank_diff <= 5 and playstyle_match:
                possible_matches.append(other_name)

    if possible_matches:
        return jsonify({"matches": possible_matches}), 200
    else:
        return jsonify({"error": "No matching players found!"}), 404

# Delete a player
@app.route('/delete_player', methods=['POST'])
def delete_player():
    data = request.get_json()
    player_name = data.get('name')

    if player_name in players:
        del players[player_name]
        return jsonify({"message": "Player deleted successfully!"}), 200
    else:
        return jsonify({"message": "Player not found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
