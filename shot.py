import pygame
from circleshape import CircleShape
from constants import SHOT_SPEED, CELL_SIZE

class Shot(CircleShape):
    def __init__(self, x, y, radius, enemy_position, target_enemy, damage):
        super().__init__(x, y, radius)
        direction = (enemy_position - self.position).normalize()
        self.velocity = direction * SHOT_SPEED
        self.target = target_enemy
        self.damage = damage
        self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile273.png"), (CELL_SIZE, CELL_SIZE))

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE // 2)


    def draw(self, screen):
        screen.blit(self.image, self.shape())
    
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
        self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile251.png"), (CELL_SIZE, CELL_SIZE))

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE // 2)


    def draw(self, screen):
        screen.blit(self.image, self.shape())
    
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
        self.image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile297.png"), (CELL_SIZE, CELL_SIZE))

    def shape(self):
        return pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE // 2)


    def draw(self, screen):
        screen.blit(self.image, self.shape())
    
    def update(self, dt, enemies=None, player=None):
        if self.target.alive():
            direction = self.target.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.velocity = direction * SHOT_SPEED
                
        self.position += self.velocity * dt