class ServerEnemy:
    def __init__(self, health, speed, x, y, path_index, damage, path_cells, owner, enemy_type="basic", wave_num=1):
        import uuid
        self.id = str(uuid.uuid4())
        self.health = health
        self.speed = speed
        self.x = x
        self.y = y
        self.path_index = path_index
        self.damage = damage
        self.path_cells = path_cells
        self.owner = owner
        self.enemy_type = enemy_type
        self.wave_num = wave_num
        self.alive = True
        self.reached_end = False
        self.in_combat = False
        self.combat_target = None

    def update(self, dt):
        if self.in_combat:
            if self.combat_target is None or not self.combat_target.alive:
                self.in_combat = False
                self.combat_target = None
            else:
                self.combat_target.health -= self.damage * dt
            return

        if self.path_index >= len(self.path_cells):
            self.reached_end = True
            self.alive = False
            return

        target = self.path_cells[self.path_index].grid_position
        dx = target.x - self.x
        dy = target.y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist > 0:
            move = self.speed * dt
            if move >= dist:
                self.x = target.x
                self.y = target.y
                self.path_index += 1
            else:
                self.x += (dx / dist) * move
                self.y += (dy / dist) * move

        if self.health <= 0:
            self.alive = False

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "owner": self.owner,
            "type": self.enemy_type,
            "path_index": self.path_index,
            "alive": self.alive,
            "reached_end": self.reached_end,
            "wave_num": self.wave_num,
        }