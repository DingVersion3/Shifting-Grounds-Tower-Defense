import pygame
from map import Map
from constants import GRID_COLS, GRID_ROWS, START, END
import random

class MapGenerator():
    def __init__(self, grid):
        self.grid = grid

    def generate_path(self):
        start_edge = random.choice(["top", "right"]) # choose the starting side 

        if start_edge == "top": #choose the start and end cell to edit based on the start_edge 
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


        start_pos = pygame.Vector2(start_column, start_row) #declaring our start and end cells position
        start_cell = self.grid[int(start_pos.y)][int(start_pos.x)]
        start_cell.cell_num = 0
        end_pos = pygame.Vector2(end_column, end_row)
        end_cell = self.grid[int(end_pos.y)][int(end_pos.x)]
        waypoints = [start_pos]
        for _ in range(3):
            wx = random.randint(2, GRID_COLS - 3)
            wy = random.randint(2, GRID_ROWS - 3)
            waypoints.append(pygame.Vector2(wx, wy))
        waypoints.append(end_pos)

        path_cells = []
        cell_count = 0
        current_pos = pygame.Vector2(start_pos.x, start_pos.y)

        for i in range(len(waypoints) - 1):
            target = waypoints[i + 1]
            
            while current_pos.x != target.x:
                cell = self.grid[int(current_pos.y)][int(current_pos.x)]
                cell.set_type("Road")
                cell.cell_num = cell_count
                path_cells.append(cell)
                cell_count += 1
                if current_pos.x < target.x:
                    current_pos.x += 1
                else:
                    current_pos.x -= 1

            while current_pos.y != target.y:
                cell = self.grid[int(current_pos.y)][int(current_pos.x)]
                cell.set_type("Road")
                cell.cell_num = cell_count
                path_cells.append(cell)
                cell_count += 1
                if current_pos.y < target.y:
                    current_pos.y += 1
                else:
                    current_pos.y -= 1

        cell = self.grid[int(end_pos.y)][int(end_pos.x)]
        cell.set_type("End")
        cell.cell_num = cell_count
        path_cells.append(cell)

        start_cell.set_type("Start")
        return path_cells


