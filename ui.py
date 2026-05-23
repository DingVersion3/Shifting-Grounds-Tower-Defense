import pygame
from constants import UI_COLOR, UI_BAR_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH

class UIBar():
    def __init__(self, screen, player, wave_manager):
        self.screen = screen
        self.player = player
        self.wave_manager = wave_manager
        self.font = pygame.font.SysFont('comicsans', 24)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - UI_BAR_HEIGHT, SCREEN_WIDTH, UI_BAR_HEIGHT)

    def draw(self, screen, selected_tower=None):
        pygame.draw.rect(screen, UI_COLOR, self.rect, 0)
        health = self.font.render(f'HEALTH: {self.player.health}', True, (255, 0 , 0))
        money = self.font.render(f'MONEY: {self.player.money}', True, (255, 0 , 0))
        current_wave = self.font.render(f'WAVE: {self.wave_manager.wave_num}', True, (255, 0 , 0))
        basic_color = (255, 255, 0) if selected_tower == "basic" else (255, 255, 255)
        jt_color = (255, 255, 0) if selected_tower == "jt" else (255, 255, 255)
        laser_color = (255, 255, 0) if selected_tower == "laser" else (255, 255, 255)
        basic_tower = self.font.render(f'BASIC TOWER 100g', True, basic_color)
        jt_tower = self.font.render(f'JT TOWER 2,000g', True, jt_color)
        laser_tower = self.font.render(f'LASER TOWER 10,000g', True, laser_color)
        self.basic_rect = basic_tower.get_rect(topleft=(200, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))
        self.jt_rect = jt_tower.get_rect(topleft=(400, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))
        self.laser_rect = laser_tower.get_rect(topleft=(600, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))
        screen.blit(health, (20, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10)) 
        screen.blit(money, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10)) 
        screen.blit(current_wave, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))
        screen.blit(basic_tower, (200, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))
        screen.blit(jt_tower, (400, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))
        screen.blit(laser_tower, (600, SCREEN_HEIGHT - UI_BAR_HEIGHT + 10))

    def handle_click(self, pos):
        if self.basic_rect.collidepoint(pos):
            return "basic"
        elif self.jt_rect.collidepoint(pos):
            return "jt"
        elif self.laser_rect.collidepoint(pos):
            return "laser"
        else:
            return None
