import pygame

class Player:
    def __init__(self):
        self.health = 3
        self.money = 0

    def earn_money(self):
        self.money += 100


    def take_damage(self):
        self.health -= 1