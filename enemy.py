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
        self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile248.png"), (CELL_SIZE, CELL_SIZE))

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def draw(self, screen):
        screen.blit(self.image, self.shape())

    def update(self, dt, enemies=None, player=None):
        if self.path_index > len(self.path_cells) -1:
            self.kill()
            player.take_damage()
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

