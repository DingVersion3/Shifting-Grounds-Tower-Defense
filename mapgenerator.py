import pygame
from map import Map
from constants import GRID_COLS, GRID_ROWS, ROAD, START, END
import random

class MapGenerator():
    def __init__(self, grid):
        self.grid = grid

    def generate_path(self):
        start_edge = random.choice(["top", "right"])

        if start_edge == "top":
            start_column = random.randint(0, GRID_COLS - 1)
            start_row = 0
            end_edge = "bottom"
        elif start_edge == "right":
            start_row = random.randint(0, GRID_ROWS - 1)
            start_column = GRID_COLS - 1
            end_edge = "left"
        if end_edge == "bottom":
            end_column = random.randint(0, GRID_COLS - 1)
            end_row = GRID_ROWS - 1
        elif end_edge == "left":
            end_row = random.randint(0, GRID_ROWS - 1)
            end_column = 0

        start_pos = pygame.Vector2(start_column, start_row)
        start_cell = self.grid[int(start_pos.y)][int(start_pos.x)]
        end_pos = pygame.Vector2(end_column, end_row)
        end_cell = self.grid[int(end_pos.y)][int(end_pos.x)]
        end_cell.cell_type = "End"
        end_cell.color = END
        current_pos = start_pos

        while current_pos != end_pos:
            if current_pos.x == 0:
                left_weight = 0
            elif end_pos.x < current_pos.x:
                left_weight = 25
            else:
                left_weight = 15

            if current_pos.x == GRID_COLS - 1:
                right_weight = 0
            elif current_pos.x < GRID_COLS - 1 and end_pos.x > current_pos.x:
                right_weight = 25
            else:
                right_weight = 15

            if current_pos.y == 0:
                up_weight = 0
            elif end_pos.y < current_pos.y:
                up_weight = 25
            else:
                up_weight = 15

            if current_pos.y == GRID_ROWS - 1:
                down_weight = 0
            elif current_pos.y < GRID_ROWS - 1 and end_pos.y > current_pos.y:
                down_weight = 25
            else:
                down_weight = 15

            direction = random.choices(["left", "right", "up", "down"], weights=[left_weight, right_weight, up_weight, down_weight])[0]
            cell = self.grid[int(current_pos.y)][int(current_pos.x)]
            cell.cell_type = "Road"
            cell.color = ROAD

            if direction == "left":
                current_pos.x -= 1
            elif direction == "right":
                current_pos.x += 1
            elif direction == "up":
                current_pos.y -= 1
            elif direction == "down":
                current_pos.y += 1
        start_cell.cell_type = "Start"
        start_cell.color = START


