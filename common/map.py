import pygame
from .constants import GRID_COLS, GRID_ROWS
from entities.cell import Cell

class Map():
    def __init__(self):
        self.columns = GRID_COLS
        self.rows = GRID_ROWS
        self.grid = [
            [Cell("Grass", pygame.Vector2(x, y)) for x in range(self.columns)] for y in range(self.rows)]

    def change_theme(self, new_type):
        for row in self.grid:
            for cell in row:
                if cell.cell_type not in ("Road", "Start", "End"):
                    cell.cell_type = new_type
                    cell._load_image()

    def draw(self, screen):
        for cells in self.grid:
            for cell in cells:
                cell.draw(screen)