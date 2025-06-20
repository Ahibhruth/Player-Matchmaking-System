import threading
import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)


class Player:
    def __init__(self, id, name, rank, playstyle, available=True, avoid=None):
        self.id = id
        self.name = name
        self.rank = rank
        self.playstyle = playstyle
        self.available = available
        self.avoid = avoid if avoid is not None else []

def player_to_dict(player):
    return {
        "id": player.id,
        "name": player.name,
        "rank": player.rank,
        "playstyle": player.playstyle,
        "available": player.available,
        "avoid": player.avoid,
    }

def dict_to_player(d):
    return Player(
        id=d["id"],
        name=d["name"],
        rank=d["rank"],
        playstyle=d["playstyle"],
        available=d.get("available", True),
        avoid=d.get("avoid", []),
    )


static_player_data = [
    {"id": 1, "name": "Alice", "rank": 1500, "playstyle": "aggressive", "available": True, "avoid": ["defensive"]},
    {"id": 2, "name": "Bob", "rank": 1480, "playstyle": "defensive", "available": True, "avoid": []},
    {"id": 3, "name": "Charlie", "rank": 1600, "playstyle": "balanced", "available": False, "avoid": ["aggressive"]},
    {"id": 4, "name": "Diana", "rank": 1430, "playstyle": "aggressive", "available": True, "avoid": []},
    {"id": 5, "name": "Eve", "rank": 1550, "playstyle": "defensive", "available": True, "avoid": ["aggressive"]},
    {"id": 6, "name": "Frank", "rank": 1700, "playstyle": "balanced", "available": False, "avoid": []},
    {"id": 7, "name": "Grace", "rank": 1450, "playstyle": "aggressive", "available": True, "avoid": []},
    {"id": 8, "name": "Hank", "rank": 1495, "playstyle": "defensive", "available": True, "avoid": []},
    {"id": 9, "name": "Ivy", "rank": 1670, "playstyle": "balanced", "available": False, "avoid": []},
    {"id": 10, "name": "Jack", "rank": 1620, "playstyle": "aggressive", "available": True, "avoid": ["defensive"]},
    {"id": 11, "name": "Karen", "rank": 1380, "playstyle": "defensive", "available": True, "avoid": []},
    {"id": 12, "name": "Leo", "rank": 1465, "playstyle": "balanced", "available": True, "avoid": []},
    {"id": 13, "name": "Mona", "rank": 1400, "playstyle": "aggressive", "available": True, "avoid": []},
    {"id": 14, "name": "Nate", "rank": 1505, "playstyle": "defensive", "available": False, "avoid": ["balanced"]},
    {"id": 15, "name": "Olivia", "rank": 1530, "playstyle": "balanced", "available": True, "avoid": ["aggressive"]},
    {"id": 16, "name": "Paul", "rank": 1580, "playstyle": "aggressive", "available": True, "avoid": []},
    {"id": 17, "name": "Quinn", "rank": 1420, "playstyle": "defensive", "available": False, "avoid": ["balanced"]},
    {"id": 18, "name": "Rachel", "rank": 1475, "playstyle": "balanced", "available": True, "avoid": []},
    {"id": 19, "name": "Steve", "rank": 1520, "playstyle": "aggressive", "available": True, "avoid": ["defensive"]},
    {"id": 20, "name": "Tina", "rank": 1440, "playstyle": "defensive", "available": True, "avoid": []},
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_JSON_PATH = os.path.join(BASE_DIR, 'players.json')
MATCH_HISTORY_PATH = os.path.join(BASE_DIR, 'match_history.json')

player_data_lock = threading.Lock()

def load_players():
    if os.path.exists(PLAYER_JSON_PATH):
        with open(PLAYER_JSON_PATH, 'r') as f:
            return json.load(f)
    return static_player_data.copy()

def save_players(players):
    with open(PLAYER_JSON_PATH, 'w') as f:
        json.dump(players, f, indent=2)

def append_match_history(winner, loser):
    history = []
    if os.path.exists(MATCH_HISTORY_PATH):
        with open(MATCH_HISTORY_PATH, 'r') as f:
            history = json.load(f)
    history.append({
        "winner": winner,
        "loser": loser,
        "timestamp": datetime.utcnow().isoformat()
    })
    with open(MATCH_HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)


@app.route('/api/players', methods=['GET'])
def get_players():
    with player_data_lock:
        players = load_players()
    return jsonify({"players": [p["name"] for p in players]})

@app.route('/api/register_player', methods=['POST'])
def register_player():
    data = request.get_json()
    with player_data_lock:
        players = load_players()
        if any(p["name"] == data['name'] for p in players):
            return jsonify({"message": "Player already exists!"}), 400
        new_id = max((p["id"] for p in players), default=0) + 1
        data["id"] = new_id
        players.append(data)
        save_players(players)
    return jsonify({"message": "Player registered successfully!"}), 200

@app.route('/api/match/<name>', methods=['GET'])
def match_player(name):
    exclude = request.args.getlist('exclude')
    with player_data_lock:
        players = [dict_to_player(p) for p in load_players()]
    current = next((p for p in players if p.name == name), None)
    if not current:
        return jsonify({"error": "Player not found!"}), 404
    candidates = [p for p in players if p.name != name and p.available and p.name not in exclude]

    fallback_levels = [(100, True, 20), (150, True, 10), (300, False, 5), (1000, False, 0)]
    for max_rank_diff, respect_avoid, style_penalty in fallback_levels:
        valid = []
        for p in candidates:
            if abs(current.rank - p.rank) > max_rank_diff:
                continue
            if respect_avoid and (p.playstyle in current.avoid or current.playstyle in p.avoid):
                continue
            cost = abs(current.rank - p.rank)
            if current.playstyle != p.playstyle:
                cost += style_penalty
            valid.append((p, cost))
        if valid:
            best = sorted(valid, key=lambda x: x[1])[0][0]
            return jsonify({"matches": [best.name]})
    return jsonify({"error": "No match found"}), 404

@app.route('/api/report_result', methods=['POST'])
def report_result():
    data = request.get_json()
    winner_name = data.get("winner")
    loser_name = data.get("loser")

    with player_data_lock:
        players = load_players()
        winner = next((p for p in players if p['name'] == winner_name), None)
        loser = next((p for p in players if p['name'] == loser_name), None)
        if not winner or not loser:
            return jsonify({"error": "Winner or loser not found"}), 404

        winner['rank'] += 25
        loser['rank'] = max(1000, loser['rank'] - 15)
        save_players(players)
        append_match_history(winner_name, loser_name)

    return jsonify({
        "message": "Match result recorded.",
        "new_winner_rank": winner['rank'],
        "new_loser_rank": loser['rank']
    })

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    with player_data_lock:
        players = load_players()
        sorted_players = sorted(players, key=lambda x: x["rank"], reverse=True)
    return jsonify(sorted_players)

@app.route('/api/match_history', methods=['GET'])
def get_match_history():
    if os.path.exists(MATCH_HISTORY_PATH):
        with open(MATCH_HISTORY_PATH, 'r') as f:
            history = json.load(f)
    else:
        history = []
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
