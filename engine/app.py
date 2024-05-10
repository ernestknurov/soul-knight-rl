import random
import pygame
from pygame.locals import RESIZABLE, QUIT
from states.game_state import GameState
from config.config_loader import load_screen_config


class App:
    def __init__(self):
        pygame.init()
        flags = RESIZABLE
        self.running = True
        self.config = load_screen_config()
        self.screen = pygame.display.set_mode(self.config['SIZE'], flags)
        self.state = GameState(self.screen)
        pygame.display.set_caption(self.config['CAPTION'])
    

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                else: 
                    self.state.handle_event(event)

            self.state.update()
            self.state.render()
            clock.tick(30)
            pygame.display.update()
        pygame.quit()
