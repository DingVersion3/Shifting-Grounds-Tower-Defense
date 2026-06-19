import pygame
from constants import CELL_SIZE

class Cell:
    def __init__(self, cell_type, grid_position, cell_num=-1):
        self.cell_type = cell_type
        self.grid_position = grid_position
        self.cell_num = cell_num
        self._load_image()

    def shape(self):
        return pygame.Rect(self.grid_position.x * CELL_SIZE, self.grid_position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    
    def draw(self, screen):
        if hasattr(self, 'image'):
            screen.blit(self.image, self.shape())
        else:
            pygame.draw.rect(screen, "red", self.shape(), 0)

    def set_type(self, cell_type):
        self.cell_type = cell_type
        self._load_image()

    def _load_image(self):
        if self.cell_type == "Grass":
            self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile024.png"), (CELL_SIZE, CELL_SIZE))
        elif self.cell_type == "Sand":
            self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile098.png"), (CELL_SIZE, CELL_SIZE))
        elif self.cell_type == "Concrete":
            self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile034.png"), (CELL_SIZE, CELL_SIZE))
        elif self.cell_type == "Road":
            self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile093.png"), (CELL_SIZE, CELL_SIZE))
        elif self.cell_type == "Start":
            self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile065.png"), (CELL_SIZE, CELL_SIZE))
        elif self.cell_type == "End":
            self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile067.png"), (CELL_SIZE, CELL_SIZE))