import pygame
import json



def load_settings():
    try:
        with open("Endterm/TSIS3/settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "volume": 0.5,
            "sound": True,
            "difficulty": "medium"
        }

def save_settings(settings):
    with open("Endterm/TSIS3/settings.json", "w") as f:
        json.dump(settings, f)

def save_leaderboard(username, score, distance):
    try:
        with open("Endterm/TSIS3/leaderboard.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append({"name": username, "score": score, "distance": distance})
    with open("Endterm/TSIS3/leaderboard.json", "w") as f:
        json.dump(data, f)


def load_leaderboard():
    try:
        with open("Endterm/TSIS3/leaderboard.json", "r") as f:
            return json.load(f)
    except:
        return []