import pygame
from enemy import Enemy
import random

class WaveManager():
    def __init__(self, path_cells):
        self.wave_num = 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10
        self.spawn_timer = 2
        self.inbetween_waves = False
        self.path_cells = path_cells
        self.next_wave_countdown = 10

    def update(self, dt, updateable, drawable, enemies):
        if self.spawn_timer > 0:
            self.spawn_timer -= dt
        elif self.spawn_timer <= 0 and self.inbetween_waves == False:
            self.spawn_timer = 2
            self.enemy_num_spawn += 1
            self.enemy_remain -= 1
            start = self.path_cells[0].grid_position
            Enemy.containers = (updateable, drawable, enemies)
            enemy_health = 10 + (self.wave_num ** 1.7 * 3)
            enemy_speed = 2 + (self.wave_num * 0.2)
            enemy = Enemy(enemy_health, enemy_speed, start.x, start.y, 1, 1, self.path_cells)
        if self.enemy_remain <= 0:
            self.inbetween_waves = True
            self.next_wave_countdown -= dt
            if self.next_wave_countdown <= 0:
                self.wave_num += 1
                self.enemy_num_spawn = 0
                self.enemy_remain = 10 + (self.wave_num * 2)
                self.next_wave_countdown = max(2, 10 - self.wave_num)
                self.spawn_timer = max(0.5, 2 - (self.wave_num * 0.1))
                self.inbetween_waves = False



