import pygame

class GameOverScreen():
    def __init__(self, screen, wave_num):
        self.screen = screen
        self.wave_num = wave_num
        self.font = pygame.font.SysFont('comicsans', 80)
        self.running = True

    def display(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            title = self.font.render('GAME OVER', True, (255, 0 , 0))
            wave_num_text = self.font.render(f'Wave Number: {self.wave_num}', True, (255, 0, 0))
            self.screen.blit(title, (200, 150))
            self.screen.blit(wave_num_text, (250, 250))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.running = False
                        return "RESTART"
                    
            pygame.display.update()
