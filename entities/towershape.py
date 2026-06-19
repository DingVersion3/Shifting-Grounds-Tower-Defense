import pygame

from common.constants import  TOWER_HEIGHT, TOWER_WIDTH

class TowerShape(pygame.sprite.Sprite):
    def __init__(self, x, y, attack_range, fire_rate, shot_timer, damage):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.height = TOWER_HEIGHT
        self.width = TOWER_WIDTH
        self.attack_range = attack_range
        self.fire_rate = fire_rate
        self.shot_timer = shot_timer
        self.damage = damage

    def draw(self, screen):
        pass

    def update(self, dt, enemies=None):
        pass

