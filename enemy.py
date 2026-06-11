import pygame
import math
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
        
        # Store unrotated base image
        self.original_image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile248.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.image = self.original_image
        self.angle = 0

    def shape(self):
        # Center the rect on your fine-grained vector position
        # Multiplying vector positions by CELL_SIZE ensures smooth, sub-pixel rendering
        rect = self.image.get_rect()
        rect.center = (self.position.x * CELL_SIZE + CELL_SIZE // 2, self.position.y * CELL_SIZE + CELL_SIZE // 2)
        return rect

    def draw(self, screen):
        # get_rect() handles the sizing/centering changes automatically now
        screen.blit(self.image, self.shape())

    def update(self, dt, enemies=None, player=None):
        if self.path_index > len(self.path_cells) - 1:
            self.kill()
            if player:
                player.take_damage()
            return
            
        target = self.path_cells[self.path_index].grid_position
        dist = target - self.position
        
        if dist.length() > 0:
            # 1. Calculate rotation angle (0 degrees is Right, Pygame Y is flipped)
            # dist.x and dist.y give us the direction vector
            self.angle = math.degrees(math.atan2(-dist.y, dist.x))
            
            # 2. Handle Rotation (Overridden cleanly in Tank subclass)
            self.rotate_assets()

            # 3. Handle Movement
            move = dist.normalize() * self.speed * dt
            # If next move overshoots target, snap to target
            if move.length() >= dist.length():
                self.position = pygame.Vector2(target)
                self.path_index += 1
            else:
                self.position += move
                
        if dist.length() < 0.1:
            self.path_index += 1

        if self.health <= 0:
            self.kill()
            return

    def rotate_assets(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)


class Tank(Enemy):
    def __init__(self, health, speed, x, y, path_index, damage, path_cells):
        super().__init__(health, speed, x, y, path_index, damage, path_cells)
        
        # Store unrotated base parts
        self.original_body = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile268.png").convert_alpha(),(CELL_SIZE, CELL_SIZE))
        self.original_turret = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile291.png").convert_alpha(),(CELL_SIZE, CELL_SIZE))
        
        # Dynamically tracked runtime parts
        self.body = self.original_body
        self.turret = self.original_turret
        self.image = self.body  

    def rotate_assets(self):
        self.body = pygame.transform.rotate(self.original_body, self.angle)
        self.turret = pygame.transform.rotate(self.original_turret, self.angle)
        self.image = self.body  # Keeps fallback rendering uniform

    def draw(self, screen):
        # 1. Establish the universal true center point of the tank
        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2
        
        # 2. Recalculate unique rects for body and turret based on their new rotation bounds
        body_rect = self.body.get_rect(center=(center_x, center_y))
        turret_rect = self.turret.get_rect(center=(center_x, center_y))
        
        # 3. Blit safely without shifting offsets
        screen.blit(self.body, body_rect)
        screen.blit(self.turret, turret_rect)


class Airplane(Enemy):
    def __init__(self, health, speed, x, y, path_index, damage, path_cells):
        super().__init__(health, speed, x, y, path_index, damage, path_cells)

        self.original_image = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile271.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.image = self.original_image

    def rotate_assets(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self, screen):
        screen.blit(self.image, self.shape())