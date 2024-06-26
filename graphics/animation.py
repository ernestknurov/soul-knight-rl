import pygame
from pygame.locals import Color
from config.config_loader import load_animation_config


class Animation:
    def __init__(self, rect, duration=10) -> None:
        self.rect = rect
        # self.pos = rect.topleft
        # self.size = rect.size
        self.duration = duration
        self.active = True
        self.config = load_animation_config()

    def render(self, screen):
        if self.active:
            if self.duration % 2 == 0:
                pygame.draw.rect(screen, Color(self.config['COLOR']), self.rect, self.config['BORDER_WIDTH'])
        self.update()

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.active = False