import pygame
from entities.enemy import Enemy, Tank, Airplane
from common.constants import CELL_SIZE
import random

class WaveManager():
    def __init__(self, path_cells, owner="p1"):
        self.owner = owner
        self.wave_num = 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10
        self.spawn_timer = 2
        self.inbetween_waves = False
        self.path_cells = path_cells
        self.next_wave_countdown = 10
        self.tanks_spawned = 0
        self.tanks_remain = 0
        self.airplanes_spawned = 0
        self.airplanes_remain = 0
        # Setup base assets here
        self.base_enemy_surface = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile245.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.base_plane_surface = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile270.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.base_tank_body = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile268.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.base_tank_turret = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile291.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))

    def get_current_assets(self):
        enemy_img = self.base_enemy_surface
        plane_img = self.base_plane_surface
        body_img = self.base_tank_body
        turret_img = self.base_tank_turret
        # Change assets used based on wave number
        if self.wave_num >= 10 and self.wave_num < 20:
            enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile246.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        elif self.wave_num >= 50 and self.wave_num < 75:
            enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile247.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            body_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile269.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            turret_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile292.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        elif self.wave_num >= 75:
            enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile248.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            plane_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile271.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
        return {
            "enemy": enemy_img,
            "plane": plane_img,
            "tank_body": body_img,
            "tank_turret": turret_img
        }

    def tanks_for_wave(self, wave_num):
        # Spawn tanks wave 20
        if wave_num < 20:
            return 0
        return 1 + (wave_num - 20) // 2
    
    def airplane_for_wave(self, wave_num):
        # Spawn airplanes wave 50
        if wave_num < 50:
            return 0
        return 1 + (wave_num - 50) // 2

    def start_next_wave(self):
        self.wave_num += 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10 + (self.wave_num * 2)
        self.tanks_remain = self.tanks_for_wave(self.wave_num)
        self.tanks_spawned = 0
        self.airplanes_remain = self.airplane_for_wave(self.wave_num)
        self.airplanes_spawned = 0
        self.next_wave_countdown = max(2, 10 - self.wave_num)
        self.spawn_timer = max(0.5, 2 - (self.wave_num * 0.1))
        self.inbetween_waves = False

    def spawn_enemy(self, updateable, drawable, enemies):
        start = self.path_cells[0].grid_position

        base_health = 10 + (self.wave_num ** 1.7 * 3)
        base_speed = 2 + (self.wave_num * 0.2)

        # Grab assets assigned to the wave
        current_sprites = self.get_current_assets()

        # Spawn a tank every 4th enemy while tanks remain
        spawn_tank = self.tanks_remain > 0 and self.enemy_num_spawn % 4 == 0
        # Spawn an airplane every 3rd enemy while airplanes remain
        spawn_airplane = self.airplanes_remain > 0 and self.enemy_num_spawn % 3 == 0

        if spawn_airplane:
            Airplane.containers = (updateable, drawable, enemies,)
            Airplane(
                health=base_health * 0.5,
                speed=base_speed * 1.5,
                x=start.x,
                y=start.y,
                path_index=1,
                damage=3,
                path_cells=self.path_cells,
                image=current_sprites["plane"], # Inject assets here
                owner=self.owner,
            )
            self.airplanes_remain -= 1
            self.airplanes_spawned += 1
        elif spawn_tank:
            Tank.containers = (updateable, drawable, enemies)
            Tank(
                health=base_health * 3,
                speed=base_speed * 0.6,
                x=start.x,
                y=start.y,
                path_index=1,
                damage=2,
                path_cells=self.path_cells,
                body_image=current_sprites["tank_body"],
                turret_image=current_sprites["tank_turret"],
                owner=self.owner,
            )
            self.tanks_remain -= 1
            self.tanks_spawned += 1
        else:
            Enemy.containers = (updateable, drawable, enemies)
            Enemy(
                health=base_health,
                speed=base_speed,
                x=start.x,
                y=start.y,
                path_index=1,
                damage=1,
                path_cells=self.path_cells,
                image=current_sprites["enemy"],
                owner=self.owner,
            )

    def update(self, dt, updateable, drawable, enemies):
        if self.spawn_timer > 0:
            self.spawn_timer -= dt

        elif not self.inbetween_waves:
            self.spawn_timer = 2
            self.enemy_num_spawn += 1
            self.enemy_remain -= 1
            self.spawn_enemy(updateable, drawable, enemies)

        if self.enemy_remain <= 0:
            self.inbetween_waves = True
            self.next_wave_countdown -= dt

            if self.next_wave_countdown <= 0:
                self.start_next_wave()