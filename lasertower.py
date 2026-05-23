import pygame
from towershape import TowerShape
from constants import LASER_TOWER_COLOR, CELL_SIZE, SHOT_RADIUS
from shot import Shot


class LaserTower(TowerShape):
    def __init__(self, x, y, attack_range=7, fire_rate=0.2, shot_timer=0.2, damage=10):
        super().__init__(x, y, attack_range, fire_rate, shot_timer, damage)
        self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile250.png"), (CELL_SIZE, CELL_SIZE))

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.image, self.shape())

    def update(self, dt, enemies=None, player=None):
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            for enemy in enemies:
                target = enemy.position
                dist = target - self.position
                if dist.length() <= self.attack_range:
                    Shot(self.position.x, self.position.y, SHOT_RADIUS / 2, enemy.position, enemy, self.damage)
                    self.shot_timer = self.fire_rate
                    break