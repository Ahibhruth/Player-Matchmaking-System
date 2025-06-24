import threading
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
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
    {"id": 21, "name": "Uma", "rank": 1602, "playstyle": "aggressive", "available": True, "avoid": []},
    {"id": 22, "name": "Victor", "rank": 1358, "playstyle": "aggressive", "available": False, "avoid": ["aggressive", "defensive", "balanced"]},
    {"id": 23, "name": "Wendy", "rank": 1565, "playstyle": "defensive", "available": False, "avoid": []},
    {"id": 24, "name": "Xavier", "rank": 1722, "playstyle": "balanced", "available": False, "avoid": ["aggressive"]},
    {"id": 25, "name": "Yara", "rank": 1446, "playstyle": "aggressive", "available": False, "avoid": ["aggressive", "defensive"]},
    {"id": 26, "name": "Zane", "rank": 1500, "playstyle": "defensive", "available": True, "avoid": ["balanced"]},
    {"id": 27, "name": "Amara", "rank": 1462, "playstyle": "defensive", "available": True, "avoid": ["aggressive", "balanced"]},
    {"id": 28, "name": "Brent", "rank": 1512, "playstyle": "balanced", "available": False, "avoid": ["defensive", "balanced"]},
    {"id": 29, "name": "Cleo", "rank": 1680, "playstyle": "balanced", "available": True, "avoid": ["aggressive"]},
    {"id": 30, "name": "Derek", "rank": 1484, "playstyle": "defensive", "available": False, "avoid": ["aggressive"]},
    {"id": 31, "name": "Elena", "rank": 1570, "playstyle": "defensive", "available": True, "avoid": ["aggressive", "defensive", "balanced"]},
    {"id": 32, "name": "Finn", "rank": 1693, "playstyle": "balanced", "available": False, "avoid": ["defensive"]},
    {"id": 33, "name": "Gia", "rank": 1673, "playstyle": "aggressive", "available": False, "avoid": ["aggressive", "defensive"]},
    {"id": 34, "name": "Harvey", "rank": 1381, "playstyle": "balanced", "available": True, "avoid": ["aggressive", "defensive", "balanced"]},
    {"id": 35, "name": "Isla", "rank": 1476, "playstyle": "aggressive", "available": True, "avoid": ["aggressive", "defensive"]},
    {"id": 36, "name": "Jay", "rank": 1480, "playstyle": "balanced", "available": True, "avoid": []},
    {"id": 37, "name": "Kara", "rank": 1663, "playstyle": "balanced", "available": False, "avoid": ["defensive"]},
    {"id": 38, "name": "Liam", "rank": 1705, "playstyle": "defensive", "available": False, "avoid": ["aggressive", "defensive", "balanced"]},
    {"id": 39, "name": "Mira", "rank": 1481, "playstyle": "aggressive", "available": False, "avoid": []},
    {"id": 40, "name": "Nico", "rank": 1549, "playstyle": "defensive", "available": True, "avoid": ["defensive", "balanced"]},
    {"id": 41, "name": "Opal", "rank": 1500, "playstyle": "aggressive", "available": False, "avoid": []},
    {"id": 42, "name": "Pia", "rank": 1371, "playstyle": "aggressive", "available": False, "avoid": ["defensive"]},
    {"id": 43, "name": "Quincy", "rank": 1689, "playstyle": "aggressive", "available": False, "avoid": ["defensive", "balanced"]},
    {"id": 44, "name": "Ravi", "rank": 1480, "playstyle": "defensive", "available": False, "avoid": ["defensive", "balanced"]},
    {"id": 45, "name": "Sia", "rank": 1682, "playstyle": "balanced", "available": True, "avoid": ["balanced"]},
    {"id": 46, "name": "Tom", "rank": 1650, "playstyle": "balanced", "available": False, "avoid": ["aggressive", "defensive"]},
    {"id": 47, "name": "Usha", "rank": 1433, "playstyle": "defensive", "available": False, "avoid": ["aggressive", "defensive"]},
    {"id": 48, "name": "Vik", "rank": 1579, "playstyle": "defensive", "available": False, "avoid": ["aggressive", "balanced"]},
    {"id": 49, "name": "Willa", "rank": 1743, "playstyle": "defensive", "available": True, "avoid": ["aggressive", "defensive", "balanced"]},
    {"id": 50, "name": "Xena", "rank": 1602, "playstyle": "balanced", "available": False, "avoid": ["aggressive", "balanced"]},
    {"id": 51, "name": "Yusuf", "rank": 1416, "playstyle": "aggressive", "available": False, "avoid": []},
    {"id": 52, "name": "Zara", "rank": 1688, "playstyle": "defensive", "available": False, "avoid": ["defensive", "balanced"]},
    {"id": 53, "name": "Ayan", "rank": 1479, "playstyle": "aggressive", "available": False, "avoid": ["aggressive"]},
    {"id": 54, "name": "Bella", "rank": 1552, "playstyle": "defensive", "available": False, "avoid": ["aggressive", "defensive"]},
    {"id": 55, "name": "Carl", "rank": 1461, "playstyle": "defensive", "available": False, "avoid": ["aggressive", "balanced"]},
    {"id": 56, "name": "Dina", "rank": 1542, "playstyle": "aggressive", "available": True, "avoid": ["aggressive", "defensive"]},
    {"id": 57, "name": "Eli", "rank": 1498, "playstyle": "defensive", "available": True, "avoid": ["aggressive", "defensive", "balanced"]},
    {"id": 58, "name": "Fay", "rank": 1521, "playstyle": "defensive", "available": True, "avoid": ["defensive"]},
    {"id": 59, "name": "Gus", "rank": 1528, "playstyle": "balanced", "available": True, "avoid": ["balanced"]},
    {"id": 60, "name": "Hope", "rank": 1539, "playstyle": "defensive", "available": True, "avoid": ["defensive", "balanced"]},
    {"id": 61, "name": "Ian", "rank": 1611, "playstyle": "balanced", "available": False, "avoid": ["defensive"]},
    {"id": 62, "name": "Joan", "rank": 1579, "playstyle": "aggressive", "available": False, "avoid": []},
    {"id": 63, "name": "Kyle", "rank": 1352, "playstyle": "balanced", "available": True, "avoid": []},
    {"id": 64, "name": "Luna", "rank": 1735, "playstyle": "defensive", "available": False, "avoid": ["defensive", "balanced"]},
    {"id": 65, "name": "Moe", "rank": 1422, "playstyle": "balanced", "available": True, "avoid": ["aggressive", "defensive"]},
    {"id": 66, "name": "Nina", "rank": 1661, "playstyle": "balanced", "available": False, "avoid": ["aggressive"]},
    {"id": 67, "name": "Omar", "rank": 1552, "playstyle": "aggressive", "available": False, "avoid": ["defensive", "balanced"]},
    {"id": 68, "name": "Penny", "rank": 1644, "playstyle": "defensive", "available": False, "avoid": []},
    {"id": 69, "name": "Rex", "rank": 1708, "playstyle": "balanced", "available": True, "avoid": ["defensive", "balanced"]},
    {"id": 70, "name": "Sara", "rank": 1396, "playstyle": "defensive", "available": False, "avoid": ["aggressive"]},
    {"id": 71, "name": "Toby", "rank": 1536, "playstyle": "defensive", "available": False, "avoid": []},
    {"id": 72, "name": "Umair", "rank": 1705, "playstyle": "defensive", "available": True, "avoid": []},
    {"id": 73, "name": "Viola", "rank": 1460, "playstyle": "aggressive", "available": False, "avoid": ["aggressive", "balanced"]},
    {"id": 74, "name": "Wren", "rank": 1496, "playstyle": "balanced", "available": False, "avoid": ["aggressive", "defensive"]},
    {"id": 75, "name": "Ximena", "rank": 1457, "playstyle": "aggressive", "available": False, "avoid": ["balanced"]},
    {"id": 76, "name": "Yuri", "rank": 1691, "playstyle": "balanced", "available": True, "avoid": ["aggressive"]},
    {"id": 77, "name": "Zelda", "rank": 1735, "playstyle": "balanced", "available": False, "avoid": ["defensive"]},
    {"id": 78, "name": "Aria", "rank": 1479, "playstyle": "balanced", "available": True, "avoid": []},
    {"id": 79, "name": "Brock", "rank": 1551, "playstyle": "balanced", "available": True, "avoid": ["defensive"]},
    {"id": 80, "name": "Clara", "rank": 1627, "playstyle": "balanced", "available": True, "avoid": ["aggressive", "defensive", "balanced"]},
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
        "timestamp": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
    })
    with open(MATCH_HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)

# --------- ROUTES ----------
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
            if abs(current.rank - p.rank) > float('inf'):#max_rank_diff replaced with float('inf')
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

@app.route('/api/player_stats/<name>', methods=['GET'])
def player_stats(name):
    with player_data_lock:
        players = load_players()
        player = next((p for p in players if p['name'] == name), None)

    if not player:
        return jsonify({"error": "Player not found"}), 404

    history = []
    if os.path.exists(MATCH_HISTORY_PATH):
        with open(MATCH_HISTORY_PATH, 'r') as f:
            history = json.load(f)

    player_history = [m for m in history if m['winner'] == name or m['loser'] == name]
    wins = sum(1 for m in player_history if m['winner'] == name)
    losses = sum(1 for m in player_history if m['loser'] == name)
    total = wins + losses
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0

    return jsonify({
        "name": player['name'],
        "rank": player['rank'],
        "playstyle": player['playstyle'],
        "wins": wins,
        "losses": losses,
        "total_matches": total,
        "win_rate": win_rate,
        "match_history": player_history  
    })

if __name__ == "__main__":
    app.run(debug=True)
