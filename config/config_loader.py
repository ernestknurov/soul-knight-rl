import json

def load_room_config():
    with open("config/room_config.json", "r") as file:
        data = json.load(file)
    return data

def load_screen_config():
    with open("config/screen_config.json", "r") as file:
        data = json.load(file)
    return data

def load_monster_config():
    with open("config/monster_config.json", "r") as file:
        data = json.load(file)
    return data

def load_player_config():
    with open("config/player_config.json", "r") as file:
        data = json.load(file)
    return data

def load_animation_config():
    with open("config/animation_config.json", "r") as file:
        data = json.load(file)
    return data

def load_menu_config():
    with open("config/menu_config.json", "r") as file:
        data = json.load(file)
    return data