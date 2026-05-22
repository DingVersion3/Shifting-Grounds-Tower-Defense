import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SHOT_SPEED, CELL_SIZE

class Shot(CircleShape):
    def __init__(self, x, y, radius, enemy_position, target_enemy, damage):
        super().__init__(x, y, radius)
        direction = (enemy_position - self.position).normalize()
        self.velocity = direction * SHOT_SPEED
        self.target = target_enemy
        self.damage = damage


    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x * CELL_SIZE, self.position.y * CELL_SIZE), SHOT_RADIUS)
    
    def update(self, dt, enemies=None, player=None):
        if self.target.alive():
            direction = (self.target.position - self.position).normalize()
            self.velocity = direction * SHOT_SPEED
        self.position += self.velocity *dt