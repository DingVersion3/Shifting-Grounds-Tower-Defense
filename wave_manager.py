import pygame
from enemy import Enemy, Tank
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
        self.tanks_spawned = 0
        self.tanks_remain = 0

    def _tanks_for_wave(self, wave_num):
        if wave_num < 20:
            return 0
        return 1 + (wave_num - 20) // 2

    def _start_next_wave(self):
        self.wave_num += 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10 + (self.wave_num * 2)
        self.tanks_remain = self._tanks_for_wave(self.wave_num)
        self.tanks_spawned = 0
        self.next_wave_countdown = max(2, 10 - self.wave_num)
        self.spawn_timer = max(0.5, 2 - (self.wave_num * 0.1))
        self.inbetween_waves = False

    def _spawn_enemy(self, updateable, drawable, enemies):
        start = self.path_cells[0].grid_position

        base_health = 10 + (self.wave_num ** 1.7 * 3)
        base_speed = 2 + (self.wave_num * 0.2)

        # Spawn a tank every 4th enemy while tanks remain
        spawn_tank = self.tanks_remain > 0 and self.enemy_num_spawn % 4 == 0

        if spawn_tank:
            Tank.containers = (updateable, drawable, enemies)
            Tank(
                health=base_health * 3,
                speed=base_speed * 0.6,
                x=start.x,
                y=start.y,
                path_index=1,
                damage=2,
                path_cells=self.path_cells,
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
            )

    def update(self, dt, updateable, drawable, enemies):
        if self.spawn_timer > 0:
            self.spawn_timer -= dt

        elif not self.inbetween_waves:
            self.spawn_timer = 2
            self.enemy_num_spawn += 1
            self.enemy_remain -= 1
            self._spawn_enemy(updateable, drawable, enemies)

        if self.enemy_remain <= 0:
            self.inbetween_waves = True
            self.next_wave_countdown -= dt

            if self.next_wave_countdown <= 0:
                self._start_next_wave()