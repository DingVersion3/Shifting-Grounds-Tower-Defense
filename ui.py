import pygame
from constants import UI_COLOR, UI_BAR_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH

class UIBar():
    def __init__(self, screen, player, wave_manager):
        self.screen = screen
        self.player = player
        self.wave_manager = wave_manager
        self.font = pygame.font.SysFont('sans', 24)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - UI_BAR_HEIGHT, SCREEN_WIDTH, UI_BAR_HEIGHT)

        TARGET_HEIGHT = 24 

        raw_dollar = pygame.image.load("assets/towerDefense_tile287.png").convert_alpha()
        scale_ratio = TARGET_HEIGHT / raw_dollar.get_height()
        target_width = int(raw_dollar.get_width() * scale_ratio)
        self.dollar_sign = pygame.transform.scale(raw_dollar, (target_width, TARGET_HEIGHT))

        self.digit_images = {}
        for i in range(10):
            tile_number = 276 + i
            filename = f"assets/towerDefense_tile{tile_number}.png"
            raw_digit = pygame.image.load(filename).convert_alpha()
            
            digit_ratio = TARGET_HEIGHT / raw_digit.get_height()
            digit_width = int(raw_digit.get_width() * digit_ratio)
            self.digit_images[str(i)] = pygame.transform.scale(raw_digit, (digit_width, TARGET_HEIGHT))

    # helper function to handle both pure numbers and currency
    def draw_graphical_value(self, screen, amount, start_x, start_y, show_dollar=False):
        spacing = 2
        current_x = start_x

        # only draw the dollar sign asset if requested
        if show_dollar:
            screen.blit(self.dollar_sign, (start_x, start_y))
            current_x = start_x + self.dollar_sign.get_width() + spacing

        # draw each digit asset sequentially
        value_str = str(amount)
        for digit in value_str:
            if digit in self.digit_images:
                digit_img = self.digit_images[digit]
                screen.blit(digit_img, (current_x, start_y))
                current_x += digit_img.get_width() + spacing
        
        return current_x - start_x


    def draw(self, screen, selected_tower=None):
        # draw the background
        pygame.draw.rect(screen, UI_COLOR, self.rect, 0)
        
        # text and image offsets
        text_y = SCREEN_HEIGHT - UI_BAR_HEIGHT + 5
        image_y = SCREEN_HEIGHT - UI_BAR_HEIGHT - 2  
        
        # text labels
        health_label = self.font.render('HEALTH: ', True, (255, 0 , 0))
        wave_label = self.font.render('WAVE: ', True, (255, 0 , 0))

        basic_color = (255, 255, 0) if selected_tower == "basic" else (255, 255, 255)
        jt_color = (255, 255, 0) if selected_tower == "jt" else (255, 255, 255)
        laser_color = (255, 255, 0) if selected_tower == "laser" else (255, 255, 255)

        basic_tower = self.font.render('BASIC TOWER ', True, basic_color)
        jt_tower = self.font.render('JT TOWER ', True, jt_color)
        laser_tower = self.font.render('LASER TOWER ', True, laser_color)

        # setup click collision boxes
        self.basic_rect = basic_tower.get_rect(topleft=(200, text_y))
        self.jt_rect = jt_tower.get_rect(topleft=(450, text_y))
        self.laser_rect = laser_tower.get_rect(topleft=(700, text_y))

        # blit text titles
        screen.blit(health_label, (20, text_y)) 
        screen.blit(wave_label, (SCREEN_WIDTH - 150, text_y))
        screen.blit(basic_tower, (200, text_y))
        screen.blit(jt_tower, (450, text_y))
        screen.blit(laser_tower, (700, text_y))

        # draw HEALTH using the tile graphics (No dollar sign)
        health_val_x = 20 + health_label.get_width()
        self.draw_graphical_value(screen, self.player.health, health_val_x, image_y, show_dollar=False)

        # draw WAVE using the tile graphics (No dollar sign)
        wave_val_x = (SCREEN_WIDTH - 150) + wave_label.get_width()
        self.draw_graphical_value(screen, self.wave_manager.wave_num, wave_val_x, image_y, show_dollar=False)

        # draw player money ( with dollar sign)
        self.draw_graphical_value(screen, self.player.money, SCREEN_WIDTH // 2 + 100, image_y, show_dollar=True)

        # draw tower asset prices (with dollar sign)
        basic_price_x = 200 + basic_tower.get_width()
        self.draw_graphical_value(screen, 100, basic_price_x, image_y, show_dollar=True)

        jt_price_x = 450 + jt_tower.get_width()
        self.draw_graphical_value(screen, 1000, jt_price_x, image_y, show_dollar=True)

        laser_price_x = 700 + laser_tower.get_width()
        self.draw_graphical_value(screen, 10000, laser_price_x, image_y, show_dollar=True)


    def handle_click(self, pos):
        # might need to expand collision check size here
        if self.basic_rect.collidepoint(pos):
            return "basic"
        elif self.jt_rect.collidepoint(pos):
            return "jt"
        elif self.laser_rect.collidepoint(pos):
            return "laser"
        else:
            return None
