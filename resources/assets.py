import json
import pygame
from config.config_loader import load_player_config, load_room_config

def load_image(path: str, size: list):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

def load_room_grid(path: str):
    grid = []
    with open("assets/grid_mapping.json", "r") as file:
        grid_mapping = json.load(file)

    with open(path, "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            grid.append(list(line))
    return grid, grid_mapping