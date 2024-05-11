import pygame

class GameStateManager:
    def __init__(self, game) -> None:
        self.game = game
        self.states = {}
        self.current_state = None

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if self.current_state:
            self.states[self.current_state].exit()
        self.current_state = name
        self.states[self.current_state].enter()

    def handle_event(self, event):
        if self.current_state:
            self.states[self.current_state].handle_event(event)

    def update(self):
        if self.current_state:
            self.states[self.current_state].update()

    def render(self, screen):
        if self.current_state:
            self.states[self.current_state].render(screen)