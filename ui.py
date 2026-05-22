import pygame
from constants import UI_COLOR, UI_BAR_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH

class UIBar():
    def __init__(self, screen, player, wave_manager):
        self.screen = screen
        self.player = player
        self.wave_manager = wave_manager
        self.font = pygame.font.SysFont('comicsans', 24)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - UI_BAR_HEIGHT, SCREEN_WIDTH, UI_BAR_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, UI_COLOR, self.rect, 0)
        health = self.font.render(f'HEALTH: {self.player.health}', True, (255, 0 , 0))
        money = self.font.render(f'MONEY: {self.player.money}', True, (255, 0 , 0))
        current_wave = self.font.render(f'WAVE: {self.wave_manager.wave_num}', True, (255, 0 , 0))
        screen.blit(health, (20, SCREEN_HEIGHT - UI_BAR_HEIGHT + 15)) # left
        screen.blit(money, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - UI_BAR_HEIGHT + 15)) # center
        screen.blit(current_wave, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - UI_BAR_HEIGHT + 15)) # right
