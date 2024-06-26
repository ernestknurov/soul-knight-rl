import random
import pygame
from pygame.locals import *
from entities.player import Player
from entities.monster import Monster
from entities.room import Room
from config.config_loader import *

class GameState:
    def __init__(self, game):
        self.game = game
        self.room_config = load_room_config()
        self.monster_config = load_monster_config()
        self.player_config = load_player_config()
        self.screen_config = load_screen_config()
        # Mappings
        self.key_to_direction = {K_UP: [0, -1], K_DOWN: [0, 1], K_LEFT: [-1, 0], K_RIGHT: [1, 0]}
        # Initialize placeholders for game objects
        self.room = None
        self.player = None
        self.monsters = None
        self.animations = []

    def enter(self):
        self.room = Room()
        self.player = Player(self.room_config['PLAYER_START_POSITION'])
        self.monsters = self.create_monsters(self.room_config['NUM_MONSTERS'])
        self.animations = []
        self.pressed_keys = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False}

    def create_monsters(self, amount: int) -> list:
            room_boundaries = ((self.room_config['POS'][0], self.room_config['POS'][0] + self.room_config['SIZE'][0] - self.monster_config['SIZE'][0]), 
                                (self.room_config['POS'][1], self.room_config['POS'][1] + self.room_config['SIZE'][1] - self.monster_config['SIZE'][1]))
            monsters = []
            while amount > 0:
                x = random.randint(*room_boundaries[0])
                y = random.randint(*room_boundaries[1])
                monster = Monster([x, y])
                if any(block.colliderect(monster.rect) for block in self.room.impassable_blocks) \
                    or self.player.rect.colliderect(monster.rect) \
                    or not self.room.rect.contains(monster.rect):
                    continue
                amount -= 1
                monsters.append(monster)
            return monsters
    
    def calculate_direction(self, from_obj, to_obj) -> list:
        from_center = from_obj.rect.center
        to_center = to_obj.rect.center
        diff = [from_center[0] - to_center[0], from_center[1] - to_center[1]]
        def num_to_dir(num):
            if num > 0:
                return -1
            elif num == 0:
                return 0
            else:
                return 1
        return list(map(num_to_dir, diff))
    
    def choose_direction(self, monster):
        random_dir  = [random.choice((-1, 0, 1)), random.choice((-1, 0, 1))]
        dir_to_player = self.calculate_direction(monster, self.player)
        weights = [self.monster_config['CHANCE_TO_DO_RANDOM_MOVE'], 1 - self.monster_config['CHANCE_TO_DO_RANDOM_MOVE']]
        direction = random.choices([random_dir, dir_to_player], weights=weights)[0]
        return direction
    
    def is_room_collision(self, obj):
        return not self.room.rect.contains(obj.rect) or any(obj.rect.colliderect(block) for block in self.room.impassable_blocks)
    
    def is_entities_collision(self, obj):
        entities = [self.player, *self.monsters]
        if obj in entities:
            entities.remove(obj)
        def get_area(size):
            return size[0] * size[1]
        return any(get_area(obj.rect.clip(entity.rect).size) >= 0.5 * get_area(obj.size) for entity in entities)
    
    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key in self.key_to_direction:
                self.pressed_keys[event.key] = True

            elif event.key == K_d:
                for monster in self.monsters:
                    animation = self.player.hit(monster)
                    if animation:
                        self.animations.append(animation)
                    if monster.health <= 0:
                        self.monsters.remove(monster)

            elif event.key == K_ESCAPE:
                self.game.state_manager.change_state('menu')

        elif event.type == KEYUP:
            if event.key in self.key_to_direction:
                self.pressed_keys[event.key] = False
    
    def update(self):
        # Update player and monster positions and check for collisions
        for key, pressed in self.pressed_keys.items():
            if pressed:
                direction = self.key_to_direction[key]
                self.player.move(direction, self.player.speed)
                if self.is_room_collision(self.player) or self.is_entities_collision(self.player):
                    self.player.move([-direction[0], -direction[1]], self.player.speed)

        # hiting
        for monster in self.monsters:
            animation = monster.hit(self.player)
            if animation:
                self.animations.append(animation)
            if self.player.health <= 0:
                self.player.restart()

        # moving
        for monster in self.monsters:
            direction = self.choose_direction(monster)
            monster.move(direction, monster.speed)
            if self.is_room_collision(monster) or self.is_entities_collision(monster):
                monster.move([-direction[0], -direction[1]], monster.speed)

        # updating
        self.player.update()
        for monster in self.monsters:
            monster.update()
        

    def render(self, screen):
        screen.fill(Color(self.screen_config['BACKGROUND_COLOR']))
        self.room.render(screen)
        for animation in self.animations:
            if animation.active:
                animation.render(screen)
            else:
                self.animations.remove(animation)
        for monster in self.monsters:
            monster.render(screen)
        self.player.render(screen)

    def exit(self):
        del self.player
        del self.room
        del self.monsters
