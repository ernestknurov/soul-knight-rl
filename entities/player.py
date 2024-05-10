import pygame
from pygame.locals import Color
from ui.text import EmojiText
from config.config_loader import load_player_config
from resources.assets import load_image
from graphics.animation import Animation


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.config = load_player_config()
        self.size = self.config['SIZE']

        self.health = self.config['HEALTH']
        self.damage = self.config['DAMAGE']
        self.speed = self.config['SPEED']

        self.health_bar = EmojiText(self.health * self.config['HEALTH_BAR_ICON'], self.pos, 
                                    'applecoloremoji', color=self.config['HEALTH_BAR_COLOR'])
        self.image = load_image(self.config['IMAGE'], self.size)
        self.rect = self.image.get_rect().move(*pos)
        self.hit_rect = self.rect.copy().inflate(self.config['HIT_RECT_SIZE'])

    def move(self, dir, value):
        dx = value * dir[0]
        dy = value * dir[1]
        self.rect = self.rect.move(dx, dy)
        self.hit_rect = self.hit_rect.move(dx, dy)
        self.pos[0] += dx
        self.pos[1] += dy
            
    def hit(self, monster):
        if self.hit_rect.colliderect(monster.rect):
            monster.health -= self.damage
            if monster.health <= 0:
                return None
            return Animation(monster.rect.topleft, monster.size)

    def render(self, screen):
        # Hit boxes
        pygame.draw.rect(screen, Color('black'), self.rect, width=1)
        pygame.draw.rect(screen, Color('green'), self.hit_rect, width=1)
        screen.blit(self.image, self.rect)
        if self.health:
            self.health_bar = EmojiText(self.health * self.config['HEALTH_BAR_ICON'], self.pos, 
                                        'applecoloremoji', color=self.config['HEALTH_BAR_COLOR'])
            self.health_bar.draw(screen)