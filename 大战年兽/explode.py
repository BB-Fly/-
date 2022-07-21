import image_from
import pygame


class Explode:
    def __init__(self, position, number, time):
        self.set_time = time
        self.position = position
        self.atk_able = True
        self.atk_able_boss = True
        self.sur_time = 0.2
        self.number = number
        if number == 1:
            self.img = image_from.explode1_img
            self.attack = 100
        elif number == 2:
            self.img = image_from.explode2_img
            self.attack = 75
        elif number == 3:
            self.img = image_from.explode3_img
            self.attack = 125
        elif number == 4:
            self.img = image_from.explode4_img
            self.attack = 45
        elif number == 5:
            self.img = image_from.explode5_img
            self.attack = 210
        elif number == 6:
            self.img = image_from.explode6_img
            self.attack = 60
        elif number == 7:
            self.img = image_from.explode7_img
            self.attack = 15
        elif number == 8:
            self.img = image_from.explode8_img
            self.attack = 75
        elif number == 9:
            self.img = image_from.explode9_img
            self.attack = 500
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.top = self.position[1]
        self.rect.left = self.position[0]
