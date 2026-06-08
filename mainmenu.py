import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('comicsans', 80)
        self.small_font = pygame.font.SysFont('comicsans', 40)
        self.running = True

    def display(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            title = self.font.render('Shifting Grounds Tower Defense', True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            start_text = self.small_font.render('Press S key to Start', True, (255, 255, 255))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(title, title_rect)
            self.screen.blit(start_text, start_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.running = False
                        return "START"
            pygame.display.update()