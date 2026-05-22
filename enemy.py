import pygame
from constants import CELL_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, speed, x, y, path_index, damage, path_cells):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.health = health
        self.speed = speed
        self.position = pygame.Vector2(x, y)
        self.path_index = path_index
        self.damage = damage
        self.path_cells = path_cells

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE + CELL_SIZE // 2 - 10, self.position.y * CELL_SIZE + CELL_SIZE // 2 - 5, 10, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, "black", self.shape(), 0)

    def update(self, dt, enemies=None):
        if self.path_index > len(self.path_cells) -1:
            self.kill()
            return
        target = self.path_cells[self.path_index].grid_position
        dist = target - self.position
        if dist.length() > 0:
            move = dist.normalize() * self.speed * dt
            self.position += move
        if dist.length() < 0.5:
            self.path_index += 1

        if self.health <= 0:
            self.kill()
            return

