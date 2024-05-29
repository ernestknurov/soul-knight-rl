import pygame
from pygame.locals import Color
from config.config_loader import load_room_config
from resources.assets import load_room_grid, load_image


class Room:
    def __init__(self):
        self.config = load_room_config()
        self.pos = self.config['POS']
        self.size = self.config['SIZE']
        self.rect = pygame.Rect(self.pos, self.size)
        self.grid_map, self.grid_mapping = load_room_grid(self.config['GRID_PATH'])
        self.block_to_image = {}
        self.impassable_blocks =  []
        for key, block in self.grid_mapping.items():
            self.block_to_image[key] = load_image(self.config['BLOCKS_PATH'] + f"/{block['name']}.png", self.config['CELL_SIZE'])

        self.grid = []
        num_cells = (self.size[0] // self.config['CELL_SIZE'][0], self.size[1] // self.config['CELL_SIZE'][1])
        for i in range(num_cells[1]):
            row = []
            for j in range(num_cells[0]):
                rect = pygame.Rect((self.pos[0] + self.config['CELL_SIZE'][0] * j, 
                                    self.pos[1] + self.config['CELL_SIZE'][1] * i), 
                                    self.config['CELL_SIZE'])
                row.append(rect)
                if not self.grid_mapping[self.grid_map[i][j]]['passable']:
                    self.impassable_blocks.append(rect)
            self.grid.append(row)

    def render(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                screen.blit(self.block_to_image[self.grid_map[i][j]], self.grid[i][j])

        pygame.draw.rect(screen, Color(self.config['BORDER_COLOR']), self.rect, self.config['BORDER_WIDTH'])