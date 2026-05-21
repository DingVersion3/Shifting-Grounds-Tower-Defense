import pygame
from constants import GRID_COLS, GRID_ROWS, CELL_SIZE
import random
from cell import Cell

class Map():
    def __init__(self):
        self.columns = GRID_COLS
        self.rows = GRID_ROWS
        self.grid = []
        for row in range(self.rows):
            row_list = []
            for column in range(self.columns):
                new_cell = Cell("Water", pygame.Vector2(column, row))
                row_list.append(new_cell)
            self.grid.append(row_list)

    def draw(self, screen):
        for cells in self.grid:
            for cell in cells:
                cell.draw(screen)