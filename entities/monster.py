import pygame
from pygame.locals import Color
from ui.text import EmojiText
from config.config_loader import load_monster_config
from resources.assets import load_image


class Monster:
    def __init__(self, pos):
        self.pos = pos
        self.config = load_monster_config()
        self.size = self.config['SIZE']

        self.health = self.config['HEALTH']
        self.damage = self.config['DAMAGE']
        self.speed = self.config['SPEED']

        self.health_bar = EmojiText(self.health * self.config['HEALTH_BAR_ICON'], self.pos, 
                                    'applecoloremoji', color=self.config['HEALTH_BAR_COLOR'])
        self.image = load_image(self.config['IMAGE'], self.size)
        self.rect = self.image.get_rect().move(*pos)

    def move(self, dir, value):
        dx = value * dir[0]
        dy = value * dir[1]
        self.rect = self.rect.move(dx, dy)
        self.pos[0] += dx
        self.pos[1] += dy

    def render(self, screen):
        pygame.draw.rect(screen, Color('brown'), self.rect, width=1)
        screen.blit(self.image, self.rect)
        if self.health:
            self.health_bar =  EmojiText(self.health * self.config['HEALTH_BAR_ICON'], self.pos, 
                                        'applecoloremoji', color=self.config['HEALTH_BAR_COLOR'])
            self.health_bar.draw(screen)
