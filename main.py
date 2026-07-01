import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, UI_BAR_HEIGHT, GRID_COLS
from logger import log_state
from entities.tower import Tower, JTTower, LaserTower, SniperTower
from common.map import Map
from server.mapgenerator import MapGenerator
from entities.enemy import Enemy, Tank, Airplane
from server.wave_manager import WaveManager
from entities.shot import Shot, Rocket, Laser
from entities.player import Player
from ui_states.gameover import GameOverScreen
from ui_states.ui import UIBar
from ui_states.mainmenu import MainMenu, MultiplayerMenu
from client.network_client import NetworkClient


class EnemyAssets:
    def __init__(self):
        self.cache = {}

    def get(self, wave_num):
        if wave_num not in self.cache:
            enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile245.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            plane_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile270.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            body_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile268.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            turret_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile291.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))

            if wave_num >= 10 and wave_num < 20:
                enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile246.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            elif wave_num >= 50 and wave_num < 75:
                enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile247.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
                body_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile269.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
                turret_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile292.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
            elif wave_num >= 75:
                enemy_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile248.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
                plane_img = pygame.transform.scale(pygame.image.load("assets/towerDefense_tile271.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))

            self.cache[wave_num] = {
                "enemy": enemy_img,
                "plane": plane_img,
                "tank_body": body_img,
                "tank_turret": turret_img
            }
        return self.cache[wave_num]

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
        active_enemy_sprites = {}
        enemy_assets = EnemyAssets()

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
                side_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 24)
                p1_color = (0, 255, 0) if local_side == "p1" else (255, 255, 255)
                p2_color = (0, 255, 0) if local_side == "p2" else (255, 255, 255)
                p1_label = side_font.render("P1 (YOU)" if local_side == "p1" else "P1", True, p1_color)
                p2_label = side_font.render("P2 (YOU)" if local_side == "p2" else "P2", True, p2_color)
                screen.blit(p1_label, (center_x // 2 - p1_label.get_width() // 2, 10))
                screen.blit(p2_label, (center_x + center_x // 2 - p2_label.get_width() // 2, 10))
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
            if game_mode == "MULTIPLAYER":
                if server_state and "enemies" in server_state:
                    current_ids = set()
                    for enemy_data in server_state["enemies"]:
                        eid = enemy_data["id"]
                        current_ids.add(eid)
                        if eid not in active_enemy_sprites:
                            enemy_type = enemy_data["type"]
                            wave_num = enemy_data.get("wave_num", 1)
                            assets = enemy_assets.get(wave_num)
                            x = enemy_data["x"]
                            y = enemy_data["y"]
                            owner = enemy_data["owner"]
                            if enemy_type == "tank":
                                Tank.containers = (drawable, enemies)
                                sprite = Tank(health=1, speed=1, x=x, y=y, path_index=0, damage=0,
                                            path_cells=[], body_image=assets["tank_body"],
                                            turret_image=assets["tank_turret"], owner=owner)
                            elif enemy_type == "airplane":
                                Airplane.containers = (drawable, enemies)
                                sprite = Airplane(health=1, speed=1, x=x, y=y, path_index=0, damage=0,
                                                path_cells=[], image=assets["plane"], owner=owner)
                            else:
                                Enemy.containers = (drawable, enemies)
                                sprite = Enemy(health=1, speed=1, x=x, y=y, path_index=0, damage=0,
                                            path_cells=[], image=assets["enemy"], owner=owner)
                            active_enemy_sprites[eid] = sprite
                        else:
                            sprite = active_enemy_sprites[eid]
                            prev_x = sprite.position.x
                            prev_y = sprite.position.y
                            sprite.position.x = enemy_data["x"]
                            sprite.position.y = enemy_data["y"]
                            sprite.health = enemy_data["health"]

                            dx = sprite.position.x - prev_x
                            dy = sprite.position.y - prev_y
                            if dx != 0 or dy != 0:
                                sprite.angle = math.degrees(math.atan2(-dy, dx))
                                sprite.rotate_assets()

                    for eid in list(active_enemy_sprites.keys()):
                        if eid not in current_ids:
                            active_enemy_sprites[eid].kill()
                            del active_enemy_sprites[eid]
            else:
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