import pygame
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from client.network_client import NetworkClient

class MenuButton():
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, border_color, border_thickness, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.border_radius = border_radius

    def hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.base_color

    def draw(self, surface):
        # 1. Background Fill
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=self.border_radius)
        
        # 2. Border Outline
        if self.border_thickness > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_thickness, border_radius=self.border_radius)
            
        # 3. Label Text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class ToggleButton():
    #Two-state button that displays current state and toggles on click.
    def __init__(self, x, y, width, height, labels, font, active_color, inactive_color, hover_color, border_color, border_thickness, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.labels = labels          # e.g. ("Windowed", "Fullscreen")
        self.font = font
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.border_radius = border_radius
        self.state = False            # False = labels[0], True = labels[1]
        self.hovered = False

    @property
    def current_label(self):
        return self.labels[1] if self.state else self.labels[0]

    @property
    def current_color(self):
        if self.hovered:
            return self.hover_color
        return self.active_color if self.state else self.inactive_color

    def hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=self.border_radius)
        if self.border_thickness > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_thickness, border_radius=self.border_radius)
        text_surface = self.font.render(self.current_label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                return True
        return False


class SettingsMenu():
    def __init__(self, screen):
        self.screen = screen
        # Fallback to standard color fill if image menu isn't desired over the dynamic bg
        self.dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.dim_overlay.fill((0, 0, 0, 200)) # Darken further for settings readability
        self.is_fullscreen = False

        try:
            self.font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 70)
            self.small_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 30)
            self.label_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 30)
        except:
            self.font = pygame.font.Font(None, 70)
            self.small_font = pygame.font.Font(None, 36)
            self.label_font = pygame.font.Font(None, 30)

        self.clock = pygame.time.Clock()
        self.running = True

        theme_blue   = (40, 60, 150)
        theme_hover  = (60, 90, 220)
        theme_border = (200, 200, 255)

        btn_width, btn_height = 250, 60
        center_x = SCREEN_WIDTH // 2 - (btn_width // 2)

        # --- Display mode toggle ---
        toggle_w, toggle_h = 220, 50
        toggle_x = SCREEN_WIDTH // 2 - toggle_w // 2
        toggle_y = SCREEN_HEIGHT // 2 - 40
        self.display_toggle = ToggleButton(
            toggle_x, toggle_y, toggle_w, toggle_h,
            labels=("Windowed", "Fullscreen"),
            font=self.label_font,
            active_color=(40, 130, 80),    # green when fullscreen is active
            inactive_color=(60, 60, 100),  # muted blue when windowed
            hover_color=(80, 110, 200),
            border_color=theme_border,
            border_thickness=2,
            border_radius=10,
        )

        # --- Back button ---
        self.back_btn = MenuButton(
            center_x, SCREEN_HEIGHT // 2 + 80,
            btn_width, btn_height, "Back",
            self.small_font,
            theme_blue, theme_hover, theme_border,
            border_thickness=3, border_radius=12,
        )

    def _apply_display_mode(self):
        if self.display_toggle.state:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def display(self, bg_update_callback=None):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            # Keep background rendering running if passed from main menu
            if bg_update_callback:
                bg_update_callback(dt)
            else:
                self.screen.fill("black")

            self.screen.blit(self.dim_overlay, (0, 0))

            # Title
            title = self.font.render("Settings", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180))
            self.screen.blit(title, title_rect)

            # "Display Mode" row label
            row_label = self.label_font.render("Display Mode", True, (200, 200, 255))
            row_label_rect = row_label.get_rect(
                midright=(self.display_toggle.rect.left - 20, self.display_toggle.rect.centery)
            )
            self.screen.blit(row_label, row_label_rect)

            # Hover + draw widgets
            mouse_pos = pygame.mouse.get_pos()
            self.display_toggle.hover(mouse_pos)
            self.back_btn.hover(mouse_pos)

            self.display_toggle.draw(self.screen)
            self.back_btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"

                if self.display_toggle.clicked(event):
                    self._apply_display_mode()

                if self.back_btn.clicked(event):
                    self.running = False
                    return "MENU"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return "MENU"

            pygame.display.flip()


class MultiplayerMenu():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        #string that stores the ip address for multiplayer sessions
        self.ip_input = "420.0.6.7"
        self.input_active = False

        #fonts fall back checks
        try:
            self.font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 36)
            self.label_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 30)
        except:
            self.font = pygame.Font(None, 36)
            self.label_font = pygame.Font(None, 36)

        theme_blue = (40, 60, 150)
        theme_hover = (60, 90, 220)
        theme_border = (200, 200, 255)
        btn_width, btn_height = 250, 60
        center_x = SCREEN_WIDTH // 2 - (btn_width // 2)

        self.connect_btn = MenuButton(
            center_x, SCREEN_HEIGHT // 2 + 10,
            btn_width, btn_height, "Connect",
            self.label_font, theme_blue, theme_hover, theme_border,
            border_thickness=3, border_radius=12
        )
        self.back_btn = MenuButton(
            center_x, SCREEN_HEIGHT // 2 + 90,
            btn_width, btn_height, "Back",
            self.label_font, theme_blue, theme_hover, theme_border,
            border_thickness=3, border_radius=12
        )
        self.input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80, 300, 50)

    def display(self, network_client=None):
        #pass network to the internet while player is interacting with the menu
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.screen.fill((20, 20, 20))

            #let network process background socket packets
            if network_client:
                network_client.update()
                #check if the network connected successfully
                if network_client.is_connected:
                    self.running = False
                    return "START_MULTIPLAYER_GAME"
                
            title = self.font.render("Multiplayer", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180))
            self.screen.blit(title, title_rect)

            box_border_color = (40, 130, 80) if self.input_active else (100, 100, 120)
            pygame.draw.rect(self.screen, (10, 10, 10), self.input_rect, border_radius=8) # filled dark background
            pygame.draw.rect(self.screen, box_border_color, self.input_rect, width=2, border_radius=8)

            ip_text_surf = self.label_font.render(self.ip_input, True, (255, 255, 255))
            self.screen.blit(ip_text_surf, (self.input_rect.x + 15, self.input_rect.y + 10))

            mouse_pos = pygame.mouse.get_pos()
            self.connect_btn.hover(mouse_pos)
            self.back_btn.hover(mouse_pos)

            self.connect_btn.draw(self.screen)
            self.back_btn.draw(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.input_active = self.input_rect.collidepoint(event.pos)
                if self.back_btn.clicked(event):
                    self.running = False
                    return "MENU"
                if self.connect_btn.clicked(event):
                    if network_client:
                        network_client.start_connection(self.ip_input)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return "MENU"
                    if self.input_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip_input = self.ip_input[:-1]
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            self.input_active = False
                        else:
                            if event.unicode in "0123456789." and len(self.ip_input) < 15: #max length for ip address, acccepts numbers and decimals only
                                self.ip_input += event.unicode
            pygame.display.flip()
        return "MENU"


class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        
        # --- FAKE GAME BACKGROUND INSTANCE SETUP ---
        from common.map import Map
        from server.mapgenerator import MapGenerator
        from server.wave_manager import WaveManager
        from entities.enemy import Enemy
        # 💡 Import towers and shots so we can rebind containers and spawn them
        from entities.tower import Tower, JTTower, LaserTower, SniperTower
        from entities.shot import Shot, Rocket, Laser

        self.bg_updateable = pygame.sprite.Group()
        self.bg_drawable = pygame.sprite.Group()
        self.bg_enemies = pygame.sprite.Group()
        self.bg_shots = pygame.sprite.Group() # 💡 Track background bullets

        # Isolate menu instances away from actual main.py core gameplay containers
        Enemy.containers = (self.bg_updateable, self.bg_drawable, self.bg_enemies)
        Shot.containers = (self.bg_shots, self.bg_updateable, self.bg_drawable)
        Rocket.containers = (self.bg_shots, self.bg_updateable, self.bg_drawable)
        Laser.containers = (self.bg_shots, self.bg_updateable, self.bg_drawable)
        
        # Bind all tower types to the menu sprite groups
        Tower.containers = (self.bg_updateable, self.bg_drawable)
        JTTower.containers = (self.bg_updateable, self.bg_drawable)
        LaserTower.containers = (self.bg_updateable, self.bg_drawable)
        SniperTower.containers = (self.bg_updateable, self.bg_drawable)

        self.bg_map = Map()
        self.map_gen = MapGenerator(self.bg_map.grid)
        self.path_cells = self.map_gen.generate_path()
        self.bg_wave_manager = WaveManager(self.path_cells)

        # 💡 Call our new method to populate the background with automated towers
        self._spawn_fake_towers(Tower, JTTower, LaserTower, SniperTower)

        # Translucent darkening matrix overlay to keep fonts high-contrast
        self.dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.dim_overlay.fill((0, 0, 0, 140)) # Alpha value 140 out of 255

        # Explicit font check fallback system prevents text object crashing
        try:
            self.font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 70)
            self.small_font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 30)
        except:
            self.font = pygame.font.Font(None, 70)
            self.small_font = pygame.font.Font(None, 30)
            
        self.running = True
        self.clock = pygame.time.Clock()

        btn_width, btn_height = 250, 60
        center_x = SCREEN_WIDTH // 2 - (btn_width // 2)
        start_y = SCREEN_HEIGHT // 2
        multiplayer_y = SCREEN_HEIGHT  // 2 + 80
        settings_y = SCREEN_HEIGHT // 2 + 160
        quit_y = SCREEN_HEIGHT // 2 + 240
        
        theme_blue = (40, 60, 150)
        theme_hover = (60, 90, 220)
        theme_border = (200, 200, 255)
        
        self.start_btn = MenuButton(center_x, start_y, btn_width, btn_height, "Start Game", self.small_font, theme_blue, theme_hover, theme_border, border_thickness=3, border_radius=12)
        self.multiplayer_btn = MenuButton(center_x, multiplayer_y, btn_width, btn_height, "Multiplayer", self.small_font, theme_blue, theme_hover, theme_border, border_thickness=3, border_radius=12)
        self.settings_btn = MenuButton(center_x, settings_y, btn_width, btn_height, "Settings", self.small_font, (128, 128, 128), (180, 180, 180), theme_border, border_thickness=3, border_radius=12)
        self.quit_btn = MenuButton(center_x, quit_y, btn_width, btn_height, "Quit", self.small_font, (120, 30, 30), (180, 40, 40), theme_border, border_thickness=3, border_radius=12)

    def _spawn_fake_towers(self, Basic, JT, Laser, Sniper):
        #Finds valid spots on the map grid and sprinkles a few random towers.
        import random
        tower_types = [Basic, JT, Laser, Sniper]
        
        # Gather all grid coordinates that aren't occupied by roads/paths
        valid_coords = []
        for y, row in enumerate(self.bg_map.grid):
            for x, cell in enumerate(row):
                if cell.cell_type not in ("Road", "Start", "End"):
                    valid_coords.append((x, y))
        
        # Shuffle coordinates and pick a fixed amount of spots (e.g., 6 random spots)
        random.shuffle(valid_coords)
        spots_to_place = min(10, len(valid_coords)) 
        
        for i in range(spots_to_place):
            tx, ty = valid_coords[i]
            chosen_tower_class = random.choice(tower_types)
            # Instantiate the tower; it automatically hooks into the menu container groups
            chosen_tower_class(tx, ty)

    def _update_and_draw_bg(self, dt):
        #Helper to advance and render the fake background scene frame step.
        # Update custom background logic systems
        self.bg_wave_manager.update(dt, self.bg_updateable, self.bg_drawable, self.bg_enemies)
        
        # Create a fake player object pass-through just so the tower update logic won't crash
        # when towers try to modify tracking states or earn money variables.
        class FakePlayer:
            def __init__(self): self.money = 0
            def earn_money(self): pass
        fake_player = FakePlayer()

        self.bg_updateable.update(dt, self.bg_enemies, fake_player)

        # Handle shot collisions against enemies in the menu simulation
        for enemy in self.bg_enemies:
            for shot in self.bg_shots:
                if shot.collides_with(enemy):
                    enemy.health -= shot.damage
                    shot.kill()

        # Despawn entities safely if zero health or reached the end criteria
        for enemy in self.bg_enemies:
            if enemy.health <= 0 or getattr(enemy, 'reached_end', False):
                enemy.kill()

        # Clear screen to paint map environment assets layer
        self.screen.fill("black")
        self.bg_map.draw(self.screen)
        for sprite in self.bg_drawable:
            sprite.draw(self.screen)

    def display(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # 1. Process background game tick
            self._update_and_draw_bg(dt)
            
            # 2. Add tint overlay layer
            self.screen.blit(self.dim_overlay, (0, 0))
            
            # 3. Draw UI content
            title = self.font.render('Shifting Grounds TD', True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
            self.screen.blit(title, title_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            self.start_btn.hover(mouse_pos)
            self.multiplayer_btn.hover(mouse_pos)
            self.settings_btn.hover(mouse_pos)
            self.quit_btn.hover(mouse_pos)

            self.start_btn.draw(self.screen)
            self.multiplayer_btn.draw(self.screen)
            self.settings_btn.draw(self.screen)
            self.quit_btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"
                if self.start_btn.clicked(event):
                    self.running = False
                    return "START"
                if self.quit_btn.clicked(event):
                    pygame.quit()
                    return "QUIT"
                if self.settings_btn.clicked(event):
                    settings = SettingsMenu(self.screen)
                    # Pass the drawing callback function so the simulation moves fluidly under settings panel
                    result = settings.display(bg_update_callback=self._update_and_draw_bg)
                    
                    self.screen = pygame.display.get_surface()
                    if result == "QUIT":
                        return "QUIT"
                    
                if self.multiplayer_btn.clicked(event):
                    self.running = False
                    return "MULTIPLAYER"
                        
            pygame.display.flip()
        return "MENU"