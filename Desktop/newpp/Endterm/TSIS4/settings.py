import json


def load_settings():
    try:
        with open("Endterm/TSIS4/settings.json", "r") as f:
            settings = json.load(f)
            return settings
    except:
        return {
            "snake_color": [0, 255, 0],
            "sound_enabled": True
        }

def save_settings(settings):
    with open("Endterm/TSIS4/settings.json", "w") as f:
        json.dump(settings, f, indent=4)