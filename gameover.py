import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverScreen():
    def __init__(self, screen, wave_num):
        self.screen = screen
        self.wave_num = wave_num
        self.font = pygame.Font('assets/Fonts/Kenney_Future_Narrow.ttf', 80)
        self.running = True

    def display(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            title = self.font.render('GAME OVER', True, (255, 0 , 0))
            wave_num_text = self.font.render(f'Wave Number: {self.wave_num}', True, (255, 0, 0))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            wave_rect = wave_num_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(title, title_rect)
            self.screen.blit(wave_num_text, wave_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return "QUIT"
                    elif event.key == pygame.K_r:
                        self.running = False
                        return "RESTART"
                    
            pygame.display.update()
