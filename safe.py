# prog.py
import random
import numpy as np
from scipy.optimize import linear_sum_assignment

class Player:
    def __init__(self, id, rank, playstyle, available, avoid=[]):
        self.id = id
        self.rank = rank
        self.playstyle = playstyle
        self.available = available
        self.avoid = avoid

def generate_sample_players():
    playstyles = ['aggressive', 'defensive', 'balanced']
    players = []
    for i in range(1, 11):
        rank = random.randint(1000, 2000)
        playstyle = random.choice(playstyles)
        available = random.choice([True, False])
        avoid = random.sample([ps for ps in playstyles if ps != playstyle], random.randint(0, 1))
        players.append(Player(i, rank, playstyle, available, avoid))
    return players

def calculate_cost(p1, p2, max_rank_diff=100):
    if not p1.available or not p2.available:
        return float('inf')
    if abs(p1.rank - p2.rank) > max_rank_diff:
        return float('inf')
    if p2.playstyle in p1.avoid or p1.playstyle in p2.avoid:
        return float('inf')
    cost = abs(p1.rank - p2.rank)
    if p1.playstyle != p2.playstyle:
        cost += 20
    return cost

def match_players(players):
    def build_cost_matrix(players, max_rank_diff, respect_avoid=True, style_penalty=20):
        n = len(players)
        matrix = np.full((n, n), float('inf'))
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                p1, p2 = players[i], players[j]
                if not p1.available or not p2.available:
                    continue
                if abs(p1.rank - p2.rank) > max_rank_diff:
                    continue
                if respect_avoid and (p2.playstyle in p1.avoid or p1.playstyle in p2.avoid):
                    continue
                cost = abs(p1.rank - p2.rank)
                if p1.playstyle != p2.playstyle:
                    cost += style_penalty
                matrix[i][j] = cost
        return matrix

    available_players = [p for p in players if p.available]
    n = len(available_players)
    if n < 2:
        return []

    # Fallback levels: (max_rank_diff, respect_avoid, style_penalty)
    fallback_levels = [
        (100, True, 20),   # strict
        (150, True, 10),   # relax rank
        (300, False, 5),   # ignore avoid
        (1000, False, 0)   # last resort
    ]

    for max_rank_diff, respect_avoid, style_penalty in fallback_levels:
        cost_matrix = build_cost_matrix(available_players, max_rank_diff, respect_avoid, style_penalty)
        if not np.isfinite(cost_matrix).any():
            continue
        try:
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
        except ValueError:
            continue

        matched = set()
        matches = []

        for i, j in zip(row_ind, col_ind):
            if i == j or i in matched or j in matched:
                continue
            cost = cost_matrix[i][j]
            if cost != float('inf'):
                matches.append((available_players[i], available_players[j]))
                matched.add(i)
                matched.add(j)

        if matches:
            return matches

    return []

# def match_selected_player(players, selected_player_id):
#     selected_player = None
#     for p in players:
#         if p.id == selected_player_id and p.available:
#             selected_player = p
#             break
#     if not selected_player:
#         return None

#     opponents = [p for p in players if p.available and p.id != selected_player.id]

#     if not opponents:
#         return None

#     def compute_costs(strict=True):
#         costs = []
#         for opp in opponents:
#             if strict:
#                 cost = calculate_cost(selected_player, opp)
#             else:
#                 # Fallback: ignore avoid list and rank difference
#                 if not selected_player.available or not opp.available:
#                     cost = float('inf')
#                 else:
#                     cost = abs(selected_player.rank - opp.rank)
#                     if selected_player.playstyle != opp.playstyle:
#                         cost += 20
#             costs.append(cost)
#         return costs

#     # Try strict cost
#     costs = compute_costs(strict=True)
#     min_index = np.argmin(costs)

#     if costs[min_index] == float('inf'):
#         # Fallback: relax constraints
#         costs = compute_costs(strict=False)
#         min_index = np.argmin(costs)
#         if costs[min_index] == float('inf'):
#             return None

#     return selected_player, opponents[min_index]


# def match_selected_player(players, selected_player_id):
#     selected_player = next((p for p in players if p.id == selected_player_id and p.available), None)
#     if not selected_player:
#         return None, None

#     opponents = [p for p in players if p.id != selected_player_id and p.available]
#     if not opponents:
#         return selected_player, None

#     def build_cost_vector(base_player, candidates, max_rank_diff, respect_avoid=True, style_penalty=20):
#         cost_vector = []
#         for p in candidates:
#             if abs(base_player.rank - p.rank) > max_rank_diff:
#                 cost_vector.append(float('inf'))
#                 continue
#             if respect_avoid and (p.playstyle in base_player.avoid or base_player.playstyle in p.avoid):
#                 cost_vector.append(float('inf'))
#                 continue
#             cost = abs(base_player.rank - p.rank)
#             if base_player.playstyle != p.playstyle:
#                 cost += style_penalty
#             cost_vector.append(cost)
#         return cost_vector

#     # Fallback levels: (max_rank_diff, respect_avoid, style_penalty)
#     fallback_levels = [
#         (100, True, 20),   # strict
#         (150, True, 10),   # relax rank
#         (300, False, 5),   # ignore avoid
#         (1000, False, 0)   # last resort
#     ]

#     for max_rank_diff, respect_avoid, style_penalty in fallback_levels:
#         costs = build_cost_vector(selected_player, opponents, max_rank_diff, respect_avoid, style_penalty)
#         if all(c == float('inf') for c in costs):
#             continue

#         best_index = costs.index(min(costs))
#         best_match = opponents[best_index]
#         return selected_player, best_match

#     return selected_player, None


# def run_matchmaking():
#     players = generate_sample_players()
#     matches = match_players(players)
#     return players, matches

import numpy as np
from scipy.optimize import linear_sum_assignment

class Player:
    def __init__(self, id, name, rank, playstyle, available, avoid=[]):
        self.id = id
        self.name = name
        self.rank = rank
        self.playstyle = playstyle
        self.available = available
        self.avoid = avoid

# Static list of 20 players
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

# Convert to Player objects
players_dataset = [Player(**data) for data in static_player_data]

def calculate_cost(p1, p2, max_rank_diff=100):
    if not p1.available or not p2.available:
        return float('inf')
    if abs(p1.rank - p2.rank) > max_rank_diff:
        return float('inf')
    if p2.playstyle in p1.avoid or p1.playstyle in p2.avoid:
        return float('inf')
    cost = abs(p1.rank - p2.rank)
    if p1.playstyle != p2.playstyle:
        cost += 20
    return cost

def match_players(players):
    def build_cost_matrix(players, max_rank_diff, respect_avoid=True, style_penalty=20):
        n = len(players)
        matrix = np.full((n, n), float('inf'))
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                p1, p2 = players[i], players[j]
                if not p1.available or not p2.available:
                    continue
                if abs(p1.rank - p2.rank) > max_rank_diff:
                    continue
                if respect_avoid and (p2.playstyle in p1.avoid or p1.playstyle in p2.avoid):
                    continue
                cost = abs(p1.rank - p2.rank)
                if p1.playstyle != p2.playstyle:
                    cost += style_penalty
                matrix[i][j] = cost
        return matrix

    available_players = [p for p in players if p.available]
    n = len(available_players)
    if n < 2:
        return []

    fallback_levels = [
        (100, True, 20),
        (150, True, 10),
        (300, False, 5),
        (1000, False, 0)
    ]

    for max_rank_diff, respect_avoid, style_penalty in fallback_levels:
        cost_matrix = build_cost_matrix(available_players, max_rank_diff, respect_avoid, style_penalty)
        if not np.isfinite(cost_matrix).any():
            continue
        try:
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
        except ValueError:
            continue

        matched = set()
        matches = []

        for i, j in zip(row_ind, col_ind):
            if i == j or i in matched or j in matched:
                continue
            cost = cost_matrix[i][j]
            if cost != float('inf'):
                matches.append((available_players[i], available_players[j]))
                matched.add(i)
                matched.add(j)

        if matches:
            return matches

    return []

def match_selected_player(players, selected_player_id):
    selected_player = next((p for p in players if p.id == selected_player_id and p.available), None)
    if not selected_player:
        return None, None

    opponents = [p for p in players if p.id != selected_player_id and p.available]
    if not opponents:
        return selected_player, None

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

    for max_rank_diff, respect_avoid, style_penalty in fallback_levels:
        costs = build_cost_vector(selected_player, opponents, max_rank_diff, respect_avoid, style_penalty)
        if all(c == float('inf') for c in costs):
            continue

        best_index = costs.index(min(costs))
        best_match = opponents[best_index]
        return selected_player, best_match

    return selected_player, None

def run_matchmaking():
    matches = match_players(players_dataset)
    return players_dataset, matches
