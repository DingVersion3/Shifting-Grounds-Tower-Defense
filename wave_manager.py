import pygame
from enemy import Enemy
import random

class WaveManager():
    def __init__(self, path_cells):
        self.wave_num = 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10
        self.spawn_timer = 5
        self.inbetween_waves = False
        self.path_cells = path_cells
        self.next_wave_countdown = 20

    def update(self, dt, updateable, drawable):
        if self.spawn_timer > 0:
            self.spawn_timer -= dt
        elif self.spawn_timer <= 0 and self.inbetween_waves == False:
            self.spawn_timer = 5
            self.enemy_num_spawn += 1
            self.enemy_remain -= 1
            start = self.path_cells[0].grid_position
            Enemy.containers = (updateable, drawable)
            enemy = Enemy(10, 2, start.x, start.y, 1, 10, self.path_cells)
        if self.enemy_remain <= 0 and self.wave_num <= 10:
            self.inbetween_waves = True
            self.next_wave_countdown -= 1
            if self.next_wave_countdown <= 0:
                self.wave_num += 1
                self.enemy_num_spawn = 0
                self.enemy_remain = 10
                self.next_wave_countdown = 20
                self.inbetween_waves = False


