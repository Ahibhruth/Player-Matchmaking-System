from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample player data stored in a dictionary
players = {}
players['Alice'] = {'rank': 10, 'playstyle': 'aggressive'}
players['Bob'] = {'rank': 12, 'playstyle': 'defensive'}
players['Charlie'] = {'rank': 15, 'playstyle': 'balanced'}
players['David'] = {'rank': 14, 'playstyle': 'aggressive'}
players['Eve'] = {'rank': 9, 'playstyle': 'defensive'}
players['Frank'] = {'rank': 16, 'playstyle': 'balanced'}
players['Grace'] = {'rank': 11, 'playstyle': 'aggressive'}
players['Heidi'] = {'rank': 13, 'playstyle': 'balanced'}
players['Ivan'] = {'rank': 17, 'playstyle': 'defensive'}
players['Judy'] = {'rank': 8, 'playstyle': 'aggressive'}
players['Karl'] = {'rank': 20, 'playstyle': 'balanced'}
players['Laura'] = {'rank': 18, 'playstyle': 'defensive'}
players['Mallory'] = {'rank': 21, 'playstyle': 'aggressive'}
players['Niaj'] = {'rank': 23, 'playstyle': 'defensive'}
players['Olivia'] = {'rank': 25, 'playstyle': 'balanced'}
players['Peggy'] = {'rank': 27, 'playstyle': 'aggressive'}
players['Quentin'] = {'rank': 29, 'playstyle': 'defensive'}
players['Rupert'] = {'rank': 22, 'playstyle': 'balanced'}
players['Sybil'] = {'rank': 24, 'playstyle': 'aggressive'}
players['Trudy'] = {'rank': 19, 'playstyle': 'balanced'}
players['Uma'] = {'rank': 30, 'playstyle': 'defensive'}
players['Victor'] = {'rank': 26, 'playstyle': 'aggressive'}
players['Wendy'] = {'rank': 28, 'playstyle': 'balanced'}
players['Xavier'] = {'rank': 31, 'playstyle': 'defensive'}
players['Yvonne'] = {'rank': 33, 'playstyle': 'aggressive'}
players['Zack'] = {'rank': 35, 'playstyle': 'balanced'}
players['Anya'] = {'rank': 37, 'playstyle': 'defensive'}
players['Ben'] = {'rank': 32, 'playstyle': 'aggressive'}
players['Cleo'] = {'rank': 34, 'playstyle': 'balanced'}
players['Derek'] = {'rank': 36, 'playstyle': 'aggressive'}
players['Ella'] = {'rank': 38, 'playstyle': 'defensive'}
players['Finn'] = {'rank': 39, 'playstyle': 'balanced'}
players['Gina'] = {'rank': 40, 'playstyle': 'aggressive'}
players['Henry'] = {'rank': 41, 'playstyle': 'defensive'}
players['Isla'] = {'rank': 42, 'playstyle': 'balanced'}
players['Jake'] = {'rank': 43, 'playstyle': 'aggressive'}
players['Kara'] = {'rank': 44, 'playstyle': 'defensive'}
players['Leo'] = {'rank': 45, 'playstyle': 'balanced'}
players['Mia'] = {'rank': 46, 'playstyle': 'aggressive'}
players['Noah'] = {'rank': 47, 'playstyle': 'defensive'}
players['Omar'] = {'rank': 48, 'playstyle': 'balanced'}
players['Paula'] = {'rank': 49, 'playstyle': 'aggressive'}
players['Quincy'] = {'rank': 50, 'playstyle': 'defensive'}
players['Rita'] = {'rank': 51, 'playstyle': 'balanced'}
players['Sam'] = {'rank': 52, 'playstyle': 'aggressive'}
players['Tina'] = {'rank': 53, 'playstyle': 'defensive'}
players['Umar'] = {'rank': 54, 'playstyle': 'balanced'}
players['Vera'] = {'rank': 55, 'playstyle': 'aggressive'}
players['Will'] = {'rank': 56, 'playstyle': 'defensive'}
players['Xena'] = {'rank': 57, 'playstyle': 'balanced'}
players['Yuri'] = {'rank': 58, 'playstyle': 'aggressive'}
players['Zoe'] = {'rank': 59, 'playstyle': 'defensive'}


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
