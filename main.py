import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, UI_BAR_HEIGHT
from logger import log_state
from entities.tower import Tower, JTTower, LaserTower, SniperTower
from common.map import Map
from server.mapgenerator import MapGenerator
from entities.enemy import Enemy
from server.wave_manager import WaveManager
from entities.shot import Shot, Rocket, Laser
from entities.player import Player
from ui_states.gameover import GameOverScreen
from ui_states.ui import UIBar
from ui_states.mainmenu import MainMenu


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    message_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 40) 
    skip_menu = False
    game_running = True
    while game_running:
        if not skip_menu:
            menu = MainMenu(screen)
            result = menu.display()
            if result == "QUIT":
                break
        else:
            skip_menu = False
        
        dt = 0.0 
        invalid_placement_timer = 0
        paused = False
        selected_tower = None
        placed_towers = set()

        updateable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        SniperTower.containers = (updateable, drawable)
        JTTower.containers = (updateable, drawable)
        LaserTower.containers = (updateable, drawable)
        Tower.containers = (updateable, drawable)
        Shot.containers = (shots, updateable, drawable)
        Rocket.containers = (shots, updateable, drawable)
        Laser.containers = (shots, updateable, drawable)

        game_map = Map()
        generated_map = MapGenerator(game_map.grid)
        path_cells = generated_map.generate_path()
        wave_manager = WaveManager(path_cells)
        player = Player(wave_manager)
        ui_bar = UIBar(screen, player, wave_manager)
        current_theme = "Grass"

        match_active = True
        while match_active:
            log_state()

            if wave_manager.wave_num >= 20 and current_theme != "Concrete":
                current_theme = "Concrete"
                game_map.change_theme("Concrete")
            elif wave_manager.wave_num >= 10 and wave_manager.wave_num < 20 and current_theme != "Sand":
                current_theme = "Sand"
                game_map.change_theme("Sand")
            elif wave_manager.wave_num < 10 and current_theme != "Grass":
                current_theme = "Grass"
                game_map.change_theme("Grass")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    match_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
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
                                    elif selected_tower == "sniper" and player.money >= 100000:
                                        SniperTower(tower_x, tower_y)
                                        player.money -= 100000
                                        placed_towers.add((tower_x, tower_y))
                                else:
                                    invalid_placement_timer = 60
            if paused: 
                pause_text = message_font.render("PAUSED", True, (255, 255, 255))
                screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
                pygame.display.flip()
                fps.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        match_active = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_running = False
                            match_active = False
                continue
            if player.health <= 0:
                result = GameOverScreen(screen, wave_manager.wave_num).display()
                if result == "RESTART":
                    skip_menu = True
                    match_active = False
                else:
                    game_running = False
                    match_active = False
                continue

            updateable.update(dt, enemies, player)

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
    pygame.quit()

if __name__ == "__main__":
    main()