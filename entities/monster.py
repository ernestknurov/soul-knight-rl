import pygame
from pygame.locals import Color
from ui.text import EmojiText
from config.config_loader import load_monster_config
from resources.assets import load_image
from graphics.animation import Animation


class Monster:
    def __init__(self, pos):
        self.pos = pos.copy()
        self.config = load_monster_config()
        self.size = self.config['SIZE']

        self.health = self.config['HEALTH']
        self.damage = self.config['DAMAGE']
        self.speed = self.config['SPEED']
        self.rollback = self.config['ROLLBACK']
        self.current_rollback = 0
        self.show_hit_boxes = self.config['SHOW_HIT_BOXES']

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

    def hit(self, player):
        if self.hit_rect.colliderect(player.rect):
            if self.current_rollback == 0:
                self.current_rollback = self.rollback
                player.health -= self.damage
                if player.health <= 0:
                    return None
                return Animation(player.rect)
        elif self.current_rollback > 0:
            self.current_rollback -= 1

    def update(self):
        if self.current_rollback > 0:
            self.current_rollback -= 1

    def render(self, screen):
        if self.show_hit_boxes:
            pygame.draw.rect(screen, Color('brown'), self.rect, width=1)
            pygame.draw.rect(screen, Color('yellow'), self.hit_rect, width=1)
        screen.blit(self.image, self.rect)
        if self.health:
            self.health_bar =  EmojiText(self.health * self.config['HEALTH_BAR_ICON'], self.pos, 
                                        'applecoloremoji', color=self.config['HEALTH_BAR_COLOR'])
            self.health_bar.draw(screen)
