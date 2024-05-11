import pygame
from pygame.locals import *
from ui.text import Text
from config.config_loader import load_menu_config

class MenuState:
    def __init__(self, game) -> None:
        self.game = game
        self.options = [
            "Start Game",
            "Options",
            "Exit"
        ]
        self.config = load_menu_config()
        self.current_option = 0

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.current_option = (self.current_option - 1) % len(self.options)
            elif event.key == K_DOWN:
                self.current_option = (self.current_option + 1) % len(self.options)
            elif event.key == K_RETURN:
                self.select_option()

    def select_option(self):
        selected_option = self.options[self.current_option]
        if selected_option == "Start Game":
            self.game.state_manager.change_state('game')
        if selected_option == "Options":
            self.game.state_manager.change_state('options')
        if selected_option == "Exit":
            self.exit()
            pygame.quit()

    def update(self):
        pass

    def render(self, screen):
        screen.fill(Color(self.config['BACKGROUND_COLOR']))
        Text("Menu", self.config['HEADER_POS'], 'arial', 48).draw(screen)
        position = self.config['FIRST_OPTION_POS']
        for i, option in enumerate(self.options):
            pygame.draw.rect(screen, Color(self.config['OPTION_COLOR']), (position, self.config['OPTION_SIZE']))
            if self.current_option == i:
                pygame.draw.rect(screen, Color('black'), (position, self.config['OPTION_SIZE']), 2)
            Text(option, position, 'arial').draw(screen)
            position = [position[0] + self.config['OPTIONS_GAP'][0], position[1] + self.config['OPTIONS_GAP'][1]]

    def enter(self):
        pass

    def exit(self):
        pass