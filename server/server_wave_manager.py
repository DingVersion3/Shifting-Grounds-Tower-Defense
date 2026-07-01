from server.server_enemy import ServerEnemy

class ServerWaveManager:
    def __init__(self, path_cells, owner):
        self.path_cells = path_cells
        self.owner = owner
        self.wave_num = 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10
        self.spawn_timer = 2
        self.inbetween_waves = False
        self.next_wave_countdown = 10
        self.enemies = []

    def tanks_for_wave(self, wave_num):
        if wave_num < 20:
            return 0
        return 1 + (wave_num - 20) // 2

    def airplane_for_wave(self, wave_num):
        if wave_num < 50:
            return 0
        return 1 + (wave_num - 50) // 2

    def start_next_wave(self):
        self.wave_num += 1
        self.enemy_num_spawn = 0
        self.enemy_remain = 10 + (self.wave_num * 2)
        self.next_wave_countdown = max(2, 10 - self.wave_num)
        self.spawn_timer = max(0.5, 2 - (self.wave_num * 0.1))
        self.inbetween_waves = False

    def spawn_enemy(self):
        start = self.path_cells[0].grid_position
        base_health = 10 + (self.wave_num ** 1.7 * 3)
        base_speed = 2 + (self.wave_num * 0.2)

        tanks_remain = self.tanks_for_wave(self.wave_num)
        spawn_tank = tanks_remain > 0 and self.enemy_num_spawn % 4 == 0
        airplanes_remain = self.airplane_for_wave(self.wave_num)
        spawn_airplane = airplanes_remain > 0 and self.enemy_num_spawn % 3 == 0

        if spawn_airplane:
            e = ServerEnemy(base_health * 0.5, base_speed * 1.5, start.x, start.y, 1, 3, self.path_cells, self.owner, "airplane", wave_num=self.wave_num)
        elif spawn_tank:
            e = ServerEnemy(base_health * 3, base_speed * 0.6, start.x, start.y, 1, 2, self.path_cells, self.owner, "tank", wave_num=self.wave_num)
        else:
            e = ServerEnemy(base_health, base_speed, start.x, start.y, 1, 1, self.path_cells, self.owner, "basic", wave_num=self.wave_num)

        self.enemies.append(e)

    def update(self, dt):
        if self.spawn_timer > 0:
            self.spawn_timer -= dt
        elif not self.inbetween_waves:
            self.spawn_timer = max(0.5, 2 - (self.wave_num * 0.1))
            self.enemy_num_spawn += 1
            self.enemy_remain -= 1
            self.spawn_enemy()

        # Check combat between opposing enemies — handled in server
        for enemy in self.enemies:
            enemy.update(dt)

        # Clean up dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        if self.enemy_remain <= 0 and not self.enemies:
            self.inbetween_waves = True
            self.next_wave_countdown -= dt
            if self.next_wave_countdown <= 0:
                self.start_next_wave()