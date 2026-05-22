import pygame
from constants import CELL_SIZE, GRASS, WATER, MOUNTAIN, ROAD, START, END

class Cell:
    def __init__(self, cell_type, grid_position, cell_num):
        self.cell_type = cell_type
        self.grid_position = grid_position
        self.cell_num = cell_num
        if cell_type == "Grass":
            self.color = GRASS
        elif cell_type == "Road":
            self.color = ROAD
        elif cell_type == "Mountain":
            self.color = MOUNTAIN
        elif cell_type == "Water":
            self.color = WATER
        elif cell_type == "Start":
            self.color = START
        elif cell_type == "End":
            self.color = END
        elif cell_type == "Empty":
            self.color = "white"
        else:
            self.color = "red"

    def shape(self):
        return pygame.Rect(self.grid_position.x * CELL_SIZE, self.grid_position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape(), 0)