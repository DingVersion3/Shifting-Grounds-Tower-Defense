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


class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        
        # Explicit font check fallback system prevents text object crashing
        try:
            self.font = pygame.font.SysFont('arial', 70)
            self.small_font = pygame.font.SysFont('arial', 36)
        except:
            self.font = pygame.font.Font(None, 70)
            self.small_font = pygame.font.Font(None, 36)
            
        self.running = True
        self.clock = pygame.time.Clock() # Maintain UI render loops properly

        btn_width, btn_height = 250, 60
        center_x = SCREEN_WIDTH // 2 - (btn_width // 2)
        start_y = SCREEN_HEIGHT // 2
        quit_y = SCREEN_HEIGHT // 2 + 80
        
        theme_blue = (40, 60, 150)
        theme_hover = (60, 90, 220)
        theme_border = (200, 200, 255)
        
        self.start_btn = MenuButton(center_x, start_y, btn_width, btn_height, "Start Game", self.small_font, theme_blue, theme_hover, theme_border, border_thickness=3, border_radius=12)
        self.quit_btn = MenuButton(center_x, quit_y, btn_width, btn_height, "Quit", self.small_font, (120, 30, 30), (180, 40, 40), theme_border, border_thickness=3, border_radius=12)

    def display(self):
        while self.running:
            self.clock.tick(60) # Limits resource drain while stuck inside main menu execution context
            self.screen.fill((0, 0, 0))
            
            title = self.font.render('Shifting Grounds Tower Defense', True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(title, title_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            self.start_btn.hover(mouse_pos)
            self.quit_btn.hover(mouse_pos)

            # Essential draw executions explicitly prioritized
            self.start_btn.draw(self.screen)
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.running = False
                        return "START"
                        
            pygame.display.flip()
