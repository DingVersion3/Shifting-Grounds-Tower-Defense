import pygame

class MapGenerator():
    def __init__(self, terrain_type, color, passable, placeable):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()