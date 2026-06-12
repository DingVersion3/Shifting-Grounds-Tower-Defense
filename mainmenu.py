import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

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
    """Two-state button that displays current state and toggles on click."""
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
        self.background = pygame.transform.scale(pygame.image.load("assets/menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.is_fullscreen = False

        try:
            self.font = pygame.font.SysFont('arial', 70)
            self.small_font = pygame.font.SysFont('arial', 36)
            self.label_font = pygame.font.SysFont('arial', 30)
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
        #"""Toggle between fullscreen and windowed without losing the surface reference."""
        if self.display_toggle.state:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def display(self):
        while self.running:
            self.clock.tick(60)
            self.screen.blit(self.background, (0, 0))

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


class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Explicit font check fallback system prevents text object crashing
        try:
            self.font = pygame.font.SysFont('arial', 70)
            self.small_font = pygame.font.SysFont('arial', 36)
        except:
            self.font = pygame.font.Font(None, 70)
            self.small_font = pygame.font.Font(None, 36)
            
        self.running = True
        self.clock = pygame.time.Clock()

        btn_width, btn_height = 250, 60
        center_x = SCREEN_WIDTH // 2 - (btn_width // 2)
        start_y = SCREEN_HEIGHT // 2
        quit_y = SCREEN_HEIGHT // 2 + 80
        settings_y = SCREEN_HEIGHT // 2 + 160
        
        theme_blue = (40, 60, 150)
        theme_hover = (60, 90, 220)
        theme_border = (200, 200, 255)
        
        self.start_btn = MenuButton(center_x, start_y, btn_width, btn_height, "Start Game", self.small_font, theme_blue, theme_hover, theme_border, border_thickness=3, border_radius=12)
        self.quit_btn = MenuButton(center_x, quit_y, btn_width, btn_height, "Quit", self.small_font, (120, 30, 30), (180, 40, 40), theme_border, border_thickness=3, border_radius=12)
        self.settings_btn = MenuButton(center_x, settings_y, btn_width, btn_height, "Settings", self.small_font, (128, 128, 128), (180, 180, 180), theme_border, border_thickness=3, border_radius=12)

    def display(self):
        while self.running:
            self.clock.tick(60)
            self.screen.blit(self.background, (0, 0))
            
            title = self.font.render('Shifting Grounds Tower Defense', True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
            self.screen.blit(title, title_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            self.start_btn.hover(mouse_pos)
            self.quit_btn.hover(mouse_pos)
            self.settings_btn.hover(mouse_pos)

            self.start_btn.draw(self.screen)
            self.quit_btn.draw(self.screen)
            self.settings_btn.draw(self.screen)

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
                    result = settings.display()
                    # Re-grab screen in case fullscreen toggled it
                    self.screen = pygame.display.get_surface()
                    if result == "QUIT":
                        return "QUIT"
                    # Otherwise fall back into main menu loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.running = False
                        return "START"
                        
            pygame.display.flip()