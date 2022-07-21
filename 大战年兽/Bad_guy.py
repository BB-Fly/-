import pygame
from bomb import ItemBomb
import image_from
import random
import copy
import math


class BadGuy:
    def __init__(self, number, time, position):
        self.position = position
        self.birth_time = time
        self.move_able = True
        self.skill_able = True
        self.attack_time = time
        self.number = number
        if number == 0:
            self.img = image_from.nian0_img
            self.health = 150
            self.speed = 0.15
            self.attack = 3
        elif number == 1:
            self.img = image_from.nian1_img
            self.health = 50
            self.speed = 0.2
            self.attack = 5
        elif number == 2:
            self.img = image_from.nian2_img
            self.health = 250
            self.speed = 0.1
            self.attack = 8
        elif number == 3:
            self.img = image_from.nian3_img
            self.health = 350
            self.speed = 0.36
            self.attack = 5
        elif number == 4:
            self.img = image_from.nian4_img
            self.health = 450
            self.speed = 0.1
            self.attack = 6
        elif number == 5:
            self.img = image_from.nian5_img
            self.health = 500
            self.speed = 0.075
            self.attack = 5
        elif number == 6:
            self.img = image_from.zombies1_img
            self.health = 250
            self.speed = 0.15
            self.attack = 5
        elif number == 7:
            self.img = image_from.lavae1_img
            self.health = 400
            self.speed = 0
            self.attack = 0
        elif number == 8:
            self.img = image_from.lavae2_img
            self.health = 300
            self.speed = 0.2
            self.attack = 8
        elif number == 9:
            self.img = image_from.critter1_img
            self.health = 75
            self.speed = 0.15
            self.attack = 2
        elif number == 10:
            self.img = image_from.fire_ball_img
            self.health = 1
            self.speed = 0.3
            self.attack = 12
        elif number == 11:
            self.img = image_from.dragonfly_0_img
            self.health = 900
            self.speed = 0
            self.attack = 0
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]

    def update(self, time, bad_guys):
        if self.move_able:
            self.position[0] -= self.speed
            self.rect.top = self.position[1]
            self.rect.left = self.position[0]
            if self.number == 6:
                if self.skill_able:
                    self.position[1] += self.speed
                else:
                    self.position[1] -= self.speed
                if self.position[1] >= 420:
                    self.skill_able = False
                elif self.position[1] <= 40:
                    self.skill_able = True
        if self.number == 3:
            if self.speed >= 0.18 and time - self.birth_time >= 2:
                self.birth_time = time
                self.speed -= 0.09
        elif self.number == 4:
            if self.move_able and self.position[0] <= 480:
                self.move_able = False
            elif time - self.birth_time >= 3.2:
                bad_guys.append(BadGuy(1, time, [self.position[0]-50, self.position[1]+30]))
                self.birth_time = time
        elif self.number == 5:
            if self.move_able and self.position[0] <= 400:
                self.move_able = False
            elif time - self.birth_time >= 2.4:
                bad_guys.append(BadGuy(10, time, [self.position[0], self.position[1]+60]))
                self.birth_time = time
        elif self.number == 7:
            if time - self.birth_time >= 4 and self.health > 0:
                self.health = 0
                bad_guys.append(BadGuy(8, time, [self.position[0], self.position[1]]))

    def death(self, time, bad_guys, item_bombs):
        if self.number == 2:
            bad_guys.append(BadGuy(1, time, [self.position[0]+60, self.position[1]]))
            bad_guys.append(BadGuy(1, time, [self.position[0]+150, self.position[1]+60]))
            bad_guys.append(BadGuy(1, time, [self.position[0]+90, self.position[1]-40]))
        elif self.number == 5:
            tmp = random.randint(0, 18) % 14 + 2
            if tmp <= 9:
                item_bombs.append(ItemBomb(copy.copy(self.position), time, tmp))
        elif self.number == 8:
            bad_guys.append(BadGuy(10, time, [self.position[0], self.position[1]]))
        if random.randint(0, 100) % (100 - self.number) == 1:
            item_bombs.append(ItemBomb(copy.copy(self.position), time, random.randint(2, 9)))

    def attacking(self, health_val, time):
        self.move_able = False
        self.attack_time = time
        health_val -= self.attack
        return health_val


class Boss:
    def __init__(self, time):
        self.health = 30000
        self.set_time = time
        self.position = [620, 60]
        self.target = None
        self.number = 0
        self.normal_img = image_from.boss_normal_img
        self.angry_img = image_from.boss_angry_img
        self.rect = pygame.Rect(self.normal_img.get_rect())
        self.count = 0

    def update(self, time, bad_guys):
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        if self.number == 0:
            if time - self.set_time <= 8:
                self.position[0] -= 0.15
            else:
                self.number = random.randint(2, 5)
                self.set_time = time
        elif self.number == 1:
            self.moving()
            if time - self.set_time >= 9:
                self.set_time = time
                self.number = random.randint(2, 5)
        elif self.number == 2:
            self.moving()
            if time - self.set_time >= 3:
                bad_guys.append(BadGuy(11, time, copy.copy(self.position)))
                self.target = None
                self.set_time = time
                self.count += 1
                if self.count >= 5:
                    self.number = 1
                    self.count = 0
        elif self.number == 3:
            if time - self.set_time >= 1.2:
                bad_guys.append(BadGuy(9, time, [640, random.randint(40, 400)]))
                self.set_time = time
                self.count += 1
                if self.count >= 14:
                    self.count = 0
                    self.number = 1
        elif self.number == 4:
            if time - self.set_time >= 3:
                if self.count == 0:
                    self.count += 1
                    bad_guys.append(BadGuy(7, time, [random.randint(0, 480)+100, random.randint(0, 320)+80]))
                    bad_guys.append(BadGuy(7, time, [random.randint(0, 480)+100, random.randint(0, 320)+80]))
                    bad_guys.append(BadGuy(7, time, [random.randint(0, 480)+100, random.randint(0, 320)+80]))
                    bad_guys.append(BadGuy(7, time, [random.randint(0, 480)+100, random.randint(0, 320)+80]))
            if time - self.set_time >= 6:
                self.number = 1
                self.set_time = time
                self.count = 0
        elif self.number == 5:
            if time - self.set_time >= 1:
                bad_guys.append(BadGuy(10, time, [self.position[0]+random.randint(0, 150), self.position[1]+random.randint(0, 150)]))
                self.set_time = time
                self.count += 1
                if self.count >= 12:
                    self.count = 0
                    self.number = 1

    def moving(self):
        if not self.target:
            self.target = [random.randint(200, 480), random.randint(0, 200)]
        else:
            direction = math.atan2(self.target[1]-(self.position[1]), self.target[0]-(self.position[0]))
            self.position[0] += 0.3*math.cos(direction)
            self.position[1] += 0.3*math.sin(direction)
            tmp = abs(self.position[0]-self.target[0]) + abs(self.position[1] - self.target[1])
            if tmp <= 5:
                self.target = None
