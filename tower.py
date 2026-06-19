import pygame
import math
from towershape import TowerShape
from constants import CELL_SIZE, SHOT_RADIUS
from shot import Shot, Rocket, Laser


class Tower(TowerShape):
    def __init__(self, x, y, attack_range=5, fire_rate=1, shot_timer=1, damage=3):
        super().__init__(x, y, attack_range, fire_rate, shot_timer, damage)
        self.base = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile181.png"), (CELL_SIZE, CELL_SIZE))
        self.original_turret = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile204.png"), (CELL_SIZE, CELL_SIZE))
        self.turret = self.original_turret
        self.angle = 0

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.base, self.shape())
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        turret_rect = self.turret.get_rect(center=(center_x, center_y))
        screen.blit(self.turret, turret_rect)

    def update(self, dt, enemies=None, player=None):
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            for enemy in enemies:
                target = enemy.position
                dist = target - self.position
                if dist.length() <= self.attack_range:
                    self.angle = math.degrees(math.atan2(-dist.y, dist.x)) - 90
                    self.turret = pygame.transform.rotozoom(self.original_turret, self.angle, 1)
                    Shot(self.position.x, self.position.y, SHOT_RADIUS, enemy.position, enemy, self.damage)
                    self.shot_timer = self.fire_rate
                    break

class JTTower(TowerShape):
    def __init__(self, x, y, attack_range=4, fire_rate=3, shot_timer=3, damage=15):
        super().__init__(x, y, attack_range, fire_rate, shot_timer, damage)
        self.base = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile183.png"), (CELL_SIZE, CELL_SIZE))
        self.original_turret = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile249.png"), (CELL_SIZE, CELL_SIZE))
        self.turret = self.original_turret
        self.angle = 0

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.base, self.shape())
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        turret_rect = self.turret.get_rect(center=(center_x, center_y))
        screen.blit(self.turret, turret_rect)

    def update(self, dt, enemies=None, player=None):
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            for enemy in enemies:
                target = enemy.position
                dist = target - self.position
                if dist.length() <= self.attack_range:
                    self.angle = math.degrees(math.atan2(-dist.y, dist.x)) - 90
                    self.turret = pygame.transform.rotozoom(self.original_turret, self.angle, 1)
                    Rocket(self.position.x, self.position.y, SHOT_RADIUS * 2, enemy.position, enemy, self.damage)
                    self.shot_timer = self.fire_rate

class LaserTower(TowerShape):
    def __init__(self, x, y, attack_range=7, fire_rate=0.2, shot_timer=0.2, damage=10):
        super().__init__(x, y, attack_range, fire_rate, shot_timer, damage)
        self.base = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile183.png"), (CELL_SIZE, CELL_SIZE))
        self.original_turret = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile250.png"), (CELL_SIZE, CELL_SIZE))
        self.turret = self.original_turret
        self.angle = 0

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.base, self.shape())
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        turret_rect = self.turret.get_rect(center=(center_x, center_y))
        screen.blit(self.turret, turret_rect)

    def update(self, dt, enemies=None, player=None):
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            for enemy in enemies:
                target = enemy.position
                dist = target - self.position
                if dist.length() <= self.attack_range:
                    self.angle = math.degrees(math.atan2(-dist.y, dist.x)) - 90
                    self.turret = pygame.transform.rotozoom(self.original_turret, self.angle, 1)
                    Laser(self.position.x, self.position.y, SHOT_RADIUS / 2, enemy.position, enemy, self.damage)
                    self.shot_timer = self.fire_rate
                    break

class SniperTower(TowerShape):
    def __init__(self, x, y, attack_range=20, fire_rate=10, shot_timer=10, damage=10000):
        super().__init__(x, y, attack_range, fire_rate, shot_timer, damage)
        self.base = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile183.png"), (CELL_SIZE, CELL_SIZE))
        self.original_turret = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile206.png"), (CELL_SIZE, CELL_SIZE))
        self.turret = self.original_turret
        self.angle = 0

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, self.width, self.height)
    
    def draw(self, screen):
        screen.blit(self.base, self.shape())
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        turret_rect = self.turret.get_rect(center=(center_x, center_y))
        screen.blit(self.turret, turret_rect)

    def update(self, dt, enemies=None, player=None):
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            for enemy in enemies:
                target = enemy.position
                dist = target - self.position
                if dist.length() <= self.attack_range:
                    self.angle = math.degrees(math.atan2(-dist.y, dist.x)) - 90
                    self.turret = pygame.transform.rotozoom(self.original_turret, self.angle, 1)
                    Laser(self.position.x, self.position.y, SHOT_RADIUS / 2, enemy.position, enemy, self.damage)
                    self.shot_timer = self.fire_rate
                    break