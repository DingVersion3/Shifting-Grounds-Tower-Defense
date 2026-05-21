import pygame
from map import Map
from constants import GRID_COLS, GRID_ROWS
import random

class MapGenerator():
    def __init__(self, grid):
        self.grid = grid

    def generate(self):
        start_edge = random.choice(["top", "right"])
        end_edge = random.choice(["bottom", "left"])

        if start_edge == "top":
            start_column = random.randint(0, GRID_COLS - 1)
            start_row = 0
        elif start_edge == "right":
            start_row = random.randint(0, GRID_ROWS - 1)
            start_column = GRID_COLS - 1

        if end_edge == "bottom":
            end_column = random.randint(0, GRID_COLS - 1)
            end_row = GRID_ROWS - 1
        elif end_edge == "left":
            end_row = random.randint(0, GRID_ROWS - 1)
            end_column = 0

        start_pos = pygame.Vector2(start_column, start_row)
        end_pos = pygame.Vector2(end_column, end_row)
