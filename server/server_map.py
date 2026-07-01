import pygame

class ServerCell:
    def __init__(self, cell_type, grid_position, cell_num=-1):
        self.cell_type = cell_type
        self.grid_position = grid_position
        self.cell_num = cell_num

    def set_type(self, cell_type):
        self.cell_type = cell_type

class ServerMap:
    def __init__(self, cols, rows):
        self.columns = cols
        self.rows = rows
        self.grid = [
            [ServerCell("Grass", pygame.Vector2(x, y)) for x in range(cols)]
            for y in range(rows)
        ]