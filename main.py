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
from mainmenu import MainMenu


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    dt = 0.0
    message_font = pygame.font.SysFont('comicsans', 40)  
    invalid_placement_timer = 0                           

    menu = MainMenu(screen)
    result = menu.display()
    if result == "QUIT":
        return

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
    player = Player(wave_manager)
    ui_bar = UIBar(screen, player, wave_manager)
    selected_tower = None
    placed_towers = set()
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
                            if cell.cell_type not in ("Road", "Start", "End") and (tower_x, tower_y) not in placed_towers:
                                if selected_tower == "basic" and player.money >= 100:
                                    Tower(tower_x, tower_y)
                                    player.money -= 100
                                    placed_towers.add((tower_x, tower_y))
                                elif selected_tower == "jt" and player.money >= 1000:
                                    JTTower(tower_x, tower_y)
                                    player.money -= 1000
                                    placed_towers.add((tower_x, tower_y))
                                elif selected_tower == "laser" and player.money >= 10000:
                                    LaserTower(tower_x, tower_y)
                                    player.money -= 10000
                                    placed_towers.add((tower_x, tower_y))
                            else:
                                invalid_placement_timer = 60
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
        if invalid_placement_timer > 0:
            message = message_font.render('Cannot place tower here!', True, (255, 0, 0))
            screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, 50)))
            invalid_placement_timer -= 1
        if selected_tower is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            preview_x = (mouse_x // CELL_SIZE) * CELL_SIZE
            preview_y = (mouse_y // CELL_SIZE) * CELL_SIZE
            pygame.draw.rect(screen, (255, 255, 255, 128), (preview_x, preview_y, CELL_SIZE, CELL_SIZE), 2)
        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()