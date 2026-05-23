import pygame

class Player:
    def __init__(self, wave_manager):
        self.health = 3
        self.money = 200
        self.wave_manager = wave_manager

    def earn_money(self):
        self.money += 15 * self.wave_manager.wave_num


    def take_damage(self):
        self.health -= 1