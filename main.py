import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, UI_BAR_HEIGHT
from logger import log_state
from tower import Tower
from jt_tower import JTTower
from lasertower import LaserTower
from map import Map
from mapgenerator import MapGenerator
from enemy import Enemy
from wave_manager import WaveManager
from shot import Shot
from player import Player
from gameover import GameOverScreen
from ui import UIBar

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    dt = 0.0
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    JTTower.containers = (updateable, drawable)
    LaserTower.containers = (updateable, drawable)
    Tower.containers = (updateable, drawable)
    Shot.containers = (shots, updateable, drawable)
    game_map = Map()
    generated_map = MapGenerator(game_map.grid)
    path_cells = generated_map.generate_path()
    wave_manager = WaveManager(path_cells)
    player = Player()
    ui_bar = UIBar(screen, player, wave_manager)
    selected_tower = None
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[1] > SCREEN_HEIGHT - UI_BAR_HEIGHT:
                        selected_tower = ui_bar.handle_click(event.pos)
                    else:
                        if selected_tower is not None:
                            tower_x = event.pos[0] // CELL_SIZE
                            tower_y = event.pos[1] // CELL_SIZE
                            cell = game_map.grid[tower_y][tower_x]
                            if cell.cell_type not in ("Road", "Start", "End"):
                                if selected_tower == "basic" and player.money >= 100:
                                    Tower(tower_x, tower_y)
                                    player.money -= 100
                                elif selected_tower == "jt" and player.money >= 250:
                                    JTTower(tower_x, tower_y)
                                    player.money -= 250
                                elif selected_tower == "laser" and player.money >= 500:
                                    LaserTower(tower_x, tower_y)
                                    player.money -= 500
        updateable.update(dt, enemies, player)
        if player.health <= 0:
            result = GameOverScreen(screen, wave_manager.wave_num).display()
            if result == "RESTART":
                main()
            return
        for enemy in enemies:
            for shot in shots:
                if shot.collides_with(enemy):
                    enemy.health -= shot.damage
                    shot.kill()
                    if enemy.health <= 0:
                        player.earn_money()
        screen.fill("black")
        game_map.draw(screen)
        ui_bar.draw(screen, selected_tower)
        wave_manager.update(dt, updateable, drawable, enemies)
        for draws in drawable:
            draws.draw(screen)
        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()