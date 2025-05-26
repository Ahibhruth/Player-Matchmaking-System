import threading
import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Player class and static dataset (from prog.py) ---
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

# Static player dataset (list of dicts)
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

# Path for persistent player data
PLAYER_JSON_PATH = os.path.join(os.path.dirname(__file__), 'players.json')

# Thread lock for safe concurrent access
player_data_lock = threading.Lock()

def load_players():
    if os.path.exists(PLAYER_JSON_PATH):
        with open(PLAYER_JSON_PATH, 'r') as f:
            return json.load(f)
    else:
        return static_player_data.copy()

def save_players(players):
    with open(PLAYER_JSON_PATH, 'w') as f:
        json.dump(players, f, indent=2)

# --- API Endpoints ---

@app.route('/api/players', methods=['GET'])
def get_players():
    with player_data_lock:
        players = load_players()
        names = [p["name"] for p in players]
    return jsonify({"players": names})

@app.route('/api/register_player', methods=['POST'])
def register_player():
    data = request.get_json()
    id_ = data.get('id')
    name = data.get('name')
    rank = data.get('rank')
    playstyle = data.get('playstyle')
    avoid = data.get('avoid', [])
    available = data.get('available', True)
    with player_data_lock:
        players = load_players()
        if any(p["name"] == name for p in players):
            return jsonify({"message": "Player already exists!"}), 400
        # Use provided id if unique, else generate new
        if id_ is None or any(p["id"] == id_ for p in players):
            new_id = max([p["id"] for p in players] or [0]) + 1
        else:
            new_id = id_
        players.append({
            "id": new_id,
            "name": name,
            "rank": rank,
            "playstyle": playstyle,
            "available": available,
            "avoid": avoid
        })
        save_players(players)
    return jsonify({"message": "Player registered successfully!"}), 200

@app.route('/api/match/<name>', methods=['GET'])
def match_player(name):
    exclude = request.args.getlist('exclude')
    if isinstance(exclude, str):
        exclude = [exclude]
    with player_data_lock:
        players = [dict_to_player(p) for p in load_players()]
    selected_player = next((p for p in players if p.name == name), None)
    if not selected_player:
        return jsonify({"error": "Player not found!"}), 404
    def build_cost_vector(base_player, candidates, max_rank_diff, respect_avoid=True, style_penalty=20):
        cost_vector = []
        for p in candidates:
            if abs(base_player.rank - p.rank) > max_rank_diff:
                cost_vector.append(float('inf'))
                continue
            if respect_avoid and (p.playstyle in base_player.avoid or base_player.playstyle in p.avoid):
                cost_vector.append(float('inf'))
                continue
            cost = abs(base_player.rank - p.rank)
            if base_player.playstyle != p.playstyle:
                cost += style_penalty
            cost_vector.append(cost)
        return cost_vector
    fallback_levels = [
        (100, True, 20),
        (150, True, 10),
        (300, False, 5),
        (1000, False, 0)
    ]
    opponents = [p for p in players if p.name != name and p.available]
    if exclude:
        opponents = [p for p in opponents if p.name not in exclude]
    for max_rank_diff, respect_avoid, style_penalty in fallback_levels:
        costs = build_cost_vector(selected_player, opponents, max_rank_diff, respect_avoid, style_penalty)
        if all(c == float('inf') for c in costs):
            continue
        best_index = costs.index(min(costs))
        best_match = opponents[best_index]
        return jsonify({"matches": [best_match.name]}), 200
    return jsonify({"error": "No matching players found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
