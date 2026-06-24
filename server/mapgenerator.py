import pygame
from common.map import Map
from common.constants import GRID_COLS, GRID_ROWS
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

    def generate_multiplayer_path(self):
        HALF_COLS = GRID_COLS // 2

        # Start on left edge, end at center
        start_row = random.randint(2, GRID_ROWS - 3)
        mid_row = random.randint(2, GRID_ROWS - 3)
        start_pos = pygame.Vector2(0, start_row)
        mid_pos = pygame.Vector2(HALF_COLS, mid_row)

        # Waypoints constrained to left half only
        waypoints = [start_pos]
        for _ in range(2):
            x = random.randint(1, HALF_COLS - 1)
            y = random.randint(2, GRID_ROWS - 3)
            waypoints.append(pygame.Vector2(x, y))
        waypoints.append(mid_pos)

        # Build left half path and track coordinates
        left_path = []
        left_coords = []
        cell_count = 0
        current_pos = pygame.Vector2(waypoints[0].x, waypoints[0].y)

        for i in range(len(waypoints) - 1):
            target = waypoints[i + 1]
            while current_pos.x != target.x:
                cell = self.grid[int(current_pos.y)][int(current_pos.x)]
                cell.set_type("Road")
                cell.cell_num = cell_count
                left_path.append(cell)
                left_coords.append((int(current_pos.x), int(current_pos.y)))
                cell_count += 1
                current_pos.x += 1 if current_pos.x < target.x else -1
            while current_pos.y != target.y:
                cell = self.grid[int(current_pos.y)][int(current_pos.x)]
                cell.set_type("Road")
                cell.cell_num = cell_count
                left_path.append(cell)
                left_coords.append((int(current_pos.x), int(current_pos.y)))
                cell_count += 1
                current_pos.y += 1 if current_pos.y < target.y else -1

        # Add midpoint
        mid_cell = self.grid[int(mid_pos.y)][int(mid_pos.x)]
        mid_cell.set_type("Road")
        mid_cell.cell_num = cell_count
        left_path.append(mid_cell)
        left_coords.append((int(mid_pos.x), int(mid_pos.y)))

        # Mirror left half to right half
        right_path = []
        for cell, (cx, cy) in zip(reversed(left_path[:-1]), 
                                reversed(left_coords[:-1])):
            mirrored_x = (GRID_COLS - 1) - cx
            right_cell = self.grid[cy][mirrored_x]
            right_cell.set_type("Road")
            right_cell.cell_num = cell_count
            right_path.append(right_cell)
            cell_count += 1

        # Full path goes left edge to center to right edge
        full_path = left_path + right_path

        full_path[0].set_type("Start")
        full_path[-1].set_type("End")

        p1_path = full_path
        p2_path = list(reversed(full_path))
        p2_path[0].set_type("Start")
        p2_path[-1].set_type("End")

        return p1_path, p2_path
    
    def path_from_waypoints(self, waypoints):
        path_cells = []
        cell_count = 0
        current_pos = pygame.Vector2(waypoints[0].x, waypoints[0].y)

        for i in range(len(waypoints) - 1):
            target = waypoints[i + 1]

            # Step horizontally
            while current_pos.x != target.x:
                cell = self.grid[int(current_pos.y)][int(current_pos.x)]
                cell.set_type("Road")
                cell.cell_num = cell_count
                path_cells.append(cell)
                cell_count += 1
                current_pos.x += 1 if current_pos.x < target.x else -1

            # Step vertically
            while current_pos.y != target.y:
                cell = self.grid[int(current_pos.y)][int(current_pos.x)]
                cell.set_type("Road")
                cell.cell_num = cell_count
                path_cells.append(cell)
                cell_count += 1
                current_pos.y += 1 if current_pos.y < target.y else -1

        # Catch the very last waypoint cell (the mid_pos)
        last_wp = waypoints[-1]
        final_cell = self.grid[int(last_wp.y)][int(last_wp.x)]
        final_cell.set_type("Road")
        final_cell.cell_num = cell_count
        path_cells.append(final_cell)

        return path_cells

