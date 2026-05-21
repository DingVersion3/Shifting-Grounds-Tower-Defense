import pygame
from towershape import TowerShape
from constants import TOWER_COLOR, TOWER_HEIGHT, TOWER_WIDTH, LINE_WIDTH


class Tower(TowerShape):
    def __init__(self, x, y, height, width):
        super().__init__(x, y, height, width)
        self.health = 100

    def shape(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, TOWER_COLOR, self.shape(), 0)