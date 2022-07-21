import pygame
import image_from
import math
import copy
from explode import Explode
import random


class Bomb:
    def __init__(self, position, direction, number, time, gap):
        self.position = copy.copy(position)
        self.direction = copy.copy(direction)
        self.number = number
        self.boom_able = False
        self.set_time = time
        self.gap = gap
        if number == 1:
            self.img = image_from.bomb1_img
            self.speed = 1.2
        elif number == 2:
            self.img = image_from.bomb2_img
            self.speed = 1.5
            self.gap = 0.2
        elif number == 3:
            self.img = image_from.bomb3_img
            self.speed = 1
        elif number == 4:
            self.img = image_from.bomb4_img
            self.speed = 0.8
        elif number == 5:
            self.img = image_from.bomb5_img
            self.speed = 1
        elif number == 6:
            self.img = image_from.bomb6_img
            self.speed = 1
        elif number == 7:
            self.img = image_from.bomb7_img
            self.speed = 1
        elif number == 8:
            self.img = image_from.bomb8_img
            self.speed = 1
        else:
            self.img = image_from.bomb9_img
            self.speed = 1
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.top = self.position[1]
        self.rect.left = self.position[0]

    def update(self, time):
        vel_x = math.cos(self.direction)*self.speed
        vel_y = math.sin(self.direction)*self.speed
        self.position[0] += vel_x
        self.position[1] += vel_y
        self.rect.top = self.position[1]
        self.rect.left = self.position[0]
        if not self.boom_able and time - self.set_time >= self.gap:
            self.boom_able = True

    def boom(self, time, explodes, bombs):
        if self.number == 1:
            explodes.append(Explode([self.position[0] + 20*math.cos(self.direction), self.position[1]+20*math.sin(self.direction)], 1, time))
        elif self.number == 2:
            explodes.append(Explode([self.position[0], self.position[1]], 2, time))
            self.boom_able = False
            self.set_time = time
        elif self.number == 3:
            explodes.append(Explode([self.position[0] - 30, self.position[1] - 30], 3, time))
        elif self.number == 4:
            explodes.append(Explode(copy.copy(self.position), 4, time))
            tmp = random.random()
            bombs.append(Bomb(copy.copy(self.position), 0, 1, time, 0.2))
            bombs.append(Bomb(copy.copy(self.position), tmp + 0.5, 1, time, 0.2))
            bombs.append(Bomb(copy.copy(self.position), tmp + 2, 1, time, 0.2))
            bombs.append(Bomb(copy.copy(self.position), tmp + 3.5, 1, time, 0.2))
        elif self.number == 5:
            explodes.append(Explode([self.position[0] - 40, self.position[1]-60], 5, time))
        elif self.number == 6:
            explodes.append(Explode([self.position[0] - 80, self.position[1]-150], 6, time))
        elif self.number == 7:
            explodes.append(Explode([self.position[0], self.position[1]], 7, time))
            bombs.append(Bomb(copy.copy(self.position), 0.9, 4, time, 0.2))
            bombs.append(Bomb(copy.copy(self.position), 5.2, 4, time, 0.2))
            bombs.append(Bomb(copy.copy(self.position), 3, 4, time, 0.2))
        elif self.number == 8:
            explodes.append(Explode([self.position[0] - 30, 0], 8, time))
            explodes.append(Explode([self.position[0] - 60, 120], 8, time))
            explodes.append(Explode([self.position[0], 240], 8, time))
            explodes.append(Explode([self.position[0] - 30, 360], 8, time))
        elif self.number == 9:
            explodes.append(Explode([self.position[0] - 30, self.position[1] - 30], 9, time))


class ItemBomb:
    def __init__(self, position, time, number):
        self.position = position
        self.set_time = time
        self.number = number
        if self.number == 2:
            self.img = image_from.bomb2_img
        elif self.number == 3:
            self.img = image_from.bomb3_img
        elif self.number == 4:
            self.img = image_from.bomb4_img
        elif self.number == 5:
            self.img = image_from.bomb5_img
        elif self.number == 6:
            self.img = image_from.bomb6_img
        elif self.number == 7:
            self.img = image_from.bomb7_img
        elif self.number == 8:
            self.img = image_from.bomb8_img
        elif self.number == 9:
            self.img = image_from.bomb9_img
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
