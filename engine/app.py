import random
import pygame
from pygame.locals import RESIZABLE, QUIT
from states.game_state import GameState
from states.menu_state import MenuState
from engine.state_manager import GameStateManager
from config.config_loader import load_screen_config


class App:
    def __init__(self):
        pygame.init()
        flags = RESIZABLE
        self.running = True
        self.config = load_screen_config()
        self.screen = pygame.display.set_mode(self.config['SIZE'], flags)
        self.state_manager = GameStateManager(self)
        self.state_manager.add_state('menu', MenuState(self))
        self.state_manager.add_state('game', GameState(self))
        self.state_manager.change_state('menu')
        pygame.display.set_caption(self.config['CAPTION'])
    

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                else: 
                    self.state_manager.handle_event(event)

            self.state_manager.update()
            self.state_manager.render(self.screen)
            clock.tick(30)
            pygame.display.update()
        pygame.quit()
