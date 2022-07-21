import pygame
import image_from
import math
from bomb import Bomb


class Player:
    def __init__(self):
        self.position = [100, 100]
        self.pos = [100, 100]
        self.able_shot = True
        self.speed = 0.8
        self.img = image_from.player_img
        self.kind_bomb = 1
        self.direction = 0
        self.pre_shot_time = 0
        self.pick_time = 0
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]

    def my_direction(self, mouse_pos):
        self.direction = math.atan2(mouse_pos[1]-(self.position[1]+32), mouse_pos[0]-(self.position[0]+26))
        if abs(self.direction) > 0.6:
            if self.direction > 0:
                self.direction = 0.6
            else:
                self.direction = -0.6
        self.img = pygame.transform.rotate(image_from.player_img, 360-self.direction*57.29)
        self.pos = (self.position[0]-self.img.get_rect().width/2, self.position[1]-self.img.get_rect().height/2)

    def update(self, time, keys):
        # player move
        if keys[0]:
            self.position[1] -= self.speed
        elif keys[2]:
            self.position[1] += self.speed
        elif keys[1]:
            self.position[0] -= self.speed
        elif keys[3]:
            self.position[0] += self.speed
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        # shoot
        if not self.able_shot:
            if time - self.pre_shot_time > 0.7:
                self.able_shot = True
        # item_bomb
        if self.kind_bomb != 1 and time - self.pick_time >= 8:
            self.kind_bomb = 1

    def set_bomb(self, bombs, time):
        if self.able_shot:
            bomb = Bomb(self.position, self.direction, self.kind_bomb, time, 0)
            bombs.append(bomb)
            self.able_shot = False
            self.pre_shot_time = time

    def pick_bomb(self, number, time):
        self.kind_bomb = number
        self.pick_time = time
