import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, UI_BAR_HEIGHT, GRID_COLS
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
from ui_states.mainmenu import MainMenu, MultiplayerMenu
from client.network_client import NetworkClient


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    message_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 40) 
    skip_menu = False
    game_running = True
    game_mode = "SINGLEPLAYER"
    network_client = NetworkClient()
    while game_running:
        if not skip_menu:
            in_menu_flow = True
            current_menu = "MAIN"
            while in_menu_flow:
                if current_menu == "MAIN":
                    menu = MainMenu(screen)
                    result = menu.display()
                    if result == "QUIT":
                        game_running = False
                        in_menu_flow = False
                    elif result == "SINGLEPLAYER" or result == "START":
                        game_mode = "SINGLEPLAYER"
                        in_menu_flow = False
                    elif result == "MULTIPLAYER":
                        current_menu = "MULTIPLAYER"
                elif current_menu == "MULTIPLAYER":
                    mp_menu = MultiplayerMenu(screen)
                    result = mp_menu.display(network_client)
                    if result == "QUIT":
                        game_running = False
                        in_menu_flow = False
                    elif result == "MENU":
                        current_menu = "MAIN"
                    elif result == "START_MULTIPLAYER_GAME":
                        game_mode = "MULTIPLAYER"
                        in_menu_flow = False
                    else:
                        current_menu = "MAIN"
        if not game_running:
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

        try:
            if game_mode == "MULTIPLAYER" and network_client is not None:
                import random
                random.seed(network_client.map_seed)
                p1_path, p2_path = generated_map.generate_multiplayer_path()
                wave_manager = WaveManager(p1_path, owner="p1")
                p2_wave_manager = WaveManager(p2_path, owner="p2")
                local_side = network_client.side
            else:
                path_cells = generated_map.generate_path()
                wave_manager = WaveManager(path_cells)
                p2_wave_manager = None
                local_side = None
        except Exception as e:
            print(f"DEBUG: CRASH DURING MAP GEN: {e}")
            continue

        player = Player(wave_manager)
        ui_bar = UIBar(screen, player, wave_manager)
        current_theme = "Grass"

        match_active = True
        print(f"DEBUG: Starting match. Mode: {game_mode}, Network Client: {network_client}")
        while match_active:
            if game_mode == "MULTIPLAYER" and network_client is not None:
                server_state = network_client.update()
            else:
                server_state = None
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
                                if game_mode == "MULTIPLAYER":
                                    on_wrong_side = (local_side == "p1" and tower_x >= GRID_COLS // 2) or \
                                                    (local_side == "p2" and tower_x < GRID_COLS // 2)
                                else:
                                    on_wrong_side = False
                                if cell.cell_type not in ("Road", "Start", "End") and (tower_x, tower_y) not in placed_towers and not on_wrong_side:
                                    if selected_tower == "basic" and player.money >= 100:
                                        Tower(tower_x, tower_y, owner=local_side)
                                        player.money -= 100
                                        placed_towers.add((tower_x, tower_y))
                                        if game_mode == "MULTIPLAYER":
                                            network_client.send_data({
                                                "action": "place_tower",
                                                "tower_type": "basic",
                                                "grid_x": tower_x,
                                                "grid_y": tower_y
                                            })
                                    elif selected_tower == "jt" and player.money >= 1000:
                                        JTTower(tower_x, tower_y, owner=local_side)
                                        player.money -= 1000
                                        placed_towers.add((tower_x, tower_y))
                                        if game_mode == "MULTIPLAYER":
                                            network_client.send_data({
                                                "action": "place_tower",
                                                "tower_type": "jt",
                                                "grid_x": tower_x,
                                                "grid_y": tower_y
                                            })
                                    elif selected_tower == "laser" and player.money >= 10000:
                                        LaserTower(tower_x, tower_y, owner=local_side)
                                        player.money -= 10000
                                        placed_towers.add((tower_x, tower_y))
                                        if game_mode == "MULTIPLAYER":
                                            network_client.send_data({
                                                "action": "place_tower",
                                                "tower_type": "laser",
                                                "grid_x": tower_x,
                                                "grid_y": tower_y
                                            })
                                    elif selected_tower == "sniper" and player.money >= 100000:
                                        SniperTower(tower_x, tower_y, owner=local_side)
                                        player.money -= 100000
                                        placed_towers.add((tower_x, tower_y))
                                        if game_mode == "MULTIPLAYER":
                                            network_client.send_data({
                                                "action": "place_tower",
                                                "tower_type": "sniper",
                                                "grid_x": tower_x,
                                                "grid_y": tower_y
                                            })
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
            
            for e1 in enemies:
                for e2 in enemies:
                    if e1.owner == e2.owner:
                        continue
                    if not e1.in_combat and not e2.in_combat:
                        if e1.shape().colliderect(e2.shape()):
                            e1.in_combat = True
                            e1.combat_target = e2
                            e2.in_combat = True
                            e2.combat_target = e1
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
            if game_mode == "MULTIPLAYER":
                center_x = (GRID_COLS // 2) * CELL_SIZE
                pygame.draw.line(screen, (255, 255, 0), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
            if server_state and "towers" in server_state:
                for tower_data in server_state["towers"]:
                    if tower_data["owner"] != network_client.player_id:
                        tx = tower_data["grid_x"]
                        ty = tower_data["grid_y"]
                        tower_type = tower_data["type"]
                        if (tx, ty) not in placed_towers:
                            placed_towers.add((tx, ty))
                            opponent_side = "p2" if local_side == "p1" else "p1"
                            if tower_type == "basic":
                                Tower(tx, ty, owner=opponent_side)
                            elif tower_type == "jt":
                                JTTower(tx, ty, owner=opponent_side)
                            elif tower_type == "laser":
                                LaserTower(tx, ty, owner=opponent_side)
                            elif tower_type == "sniper":
                                SniperTower(tx, ty, owner=opponent_side)
            ui_bar.draw(screen, selected_tower)
            wave_manager.update(dt, updateable, drawable, enemies)
            if p2_wave_manager:
                p2_wave_manager.update(dt, updateable, drawable, enemies)

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