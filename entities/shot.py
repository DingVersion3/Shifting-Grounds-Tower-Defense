import pygame
import math
from common.circleshape import CircleShape
from common.constants import SHOT_SPEED, CELL_SIZE

class Shot(CircleShape):
    def __init__(self, x, y, radius, enemy_position, target_enemy, damage):
        super().__init__(x, y, radius)
        direction = (enemy_position - self.position).normalize()
        self.velocity = direction * SHOT_SPEED
        self.target = target_enemy
        self.damage = damage
        self.original_image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile251.png"), (CELL_SIZE, CELL_SIZE))
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE // 2)


    def draw(self, screen):
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        rect = self.image.get_rect(center=(center_x, center_y))
        screen.blit(self.image, rect)
    
    def update(self, dt, enemies=None, player=None):
        if self.target.alive():
            direction = self.target.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.velocity = direction * SHOT_SPEED
                
        self.position += self.velocity * dt

class Rocket(CircleShape):
    def __init__(self, x, y, radius, enemy_position, target_enemy, damage):
        super().__init__(x, y, radius)
        direction = (enemy_position - self.position).normalize()
        self.velocity = direction * SHOT_SPEED
        self.target = target_enemy
        self.damage = damage
        self.original_image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile252.png"), (CELL_SIZE, CELL_SIZE))
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE // 2)


    def draw(self, screen):
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        rect = self.image.get_rect(center=(center_x, center_y))
        screen.blit(self.image, rect)
    
    def update(self, dt, enemies=None, player=None):
        if self.target.alive():
            direction = self.target.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.velocity = direction * SHOT_SPEED
                
        self.position += self.velocity * dt

class Laser(CircleShape):
    def __init__(self, x, y, radius, enemy_position, target_enemy, damage):
        super().__init__(x, y, radius)
        direction = (enemy_position - self.position).normalize()
        self.velocity = direction * SHOT_SPEED
        self.target = target_enemy
        self.damage = damage
        self.original_image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile297.png"), (CELL_SIZE, CELL_SIZE))
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90 + 180
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE // 2)


    def draw(self, screen):
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        rect = self.image.get_rect(center=(center_x, center_y))
        screen.blit(self.image, rect)
    
    def update(self, dt, enemies=None, player=None):
        if self.target.alive():
            direction = self.target.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.velocity = direction * SHOT_SPEED
                
        self.position += self.velocity * dt