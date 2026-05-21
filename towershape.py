import pygame

class TowerShape(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.height = height
        self.width = width

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

