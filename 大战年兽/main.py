import pygame
import image_from
from Player import Player
from pygame.locals import *
from Bad_guy import BadGuy
from Bad_guy import Boss
from bomb import ItemBomb
import random

# init
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
player = Player()
bombs = []
bad_guys = []
explodes = []
item_bombs = []
keys = [False, False, False, False]
timer = pygame.time.get_ticks()/1000
timer_1 = 100
timer_2 = 500
health_val = 150
# end or run
running = True
is_bossing = False
boss = None
exitcode = False
# game body
while running:
    # time
    now = pygame.time.get_ticks()/1000
    # background
    screen.fill(0)
    screen.blit(image_from.lawn_img, (0, 0))
    # bad guys timer
    if now - timer <= 10:
        if timer_1 <= 0:
            bad_guy = BadGuy(random.randint(0, 1), now, [640, random.randint(45, 440)])
            bad_guys.append(bad_guy)
            timer_1 = 800
        else:
            timer_1 -= 1
    elif now - timer <= 25:
        if timer_1 <= 0:
            bad_guy = BadGuy(random.randint(0, 5) % 4, now, [640, random.randint(45, 380)])
            bad_guys.append(bad_guy)
            timer_1 = 1000
        else:
            timer_1 -= 1
        if timer_2 <= 0:
            item_bombs.append(ItemBomb([100, random.randint(45, 400)], now, random.randint(2, 6)))
            timer_2 = 18000
        else:
            timer_2 -= 1
    elif now - timer <= 60:
        if timer_1 <= 0:
            bad_guy = BadGuy(random.randint(0, 7) % 6, now, [640, random.randint(45, 360)])
            bad_guys.append(bad_guy)
            timer_1 = 900
        else:
            timer_1 -= 1
        if timer_2 <= 0:
            item_bombs.append(ItemBomb([100, random.randint(45, 400)], now, random.randint(2, 6)))
            timer_2 = 15000
        else:
            timer_2 -= 1
    elif now - timer <= 90:
        if timer_1 <= 0:
            bad_guy = BadGuy(random.randint(0, 6), now, [640, random.randint(45, 360)])
            bad_guys.append(bad_guy)
            timer_1 = 750
        else:
            timer_1 -= 1
        if timer_2 <= 0:
            item_bombs.append(ItemBomb([100, random.randint(45, 400)], now, random.randint(2, 6)))
            timer_2 = 12500
        else:
            timer_2 -= 1
    else:
        if not is_bossing:
            is_bossing = True
            boss = Boss(now)
        if timer_1 <= 0:
            bad_guy = BadGuy(random.randint(0, 6), now, [640, random.randint(45, 360)])
            bad_guys.append(bad_guy)
            timer_1 = 900
        else:
            timer_1 -= 1
        if timer_2 <= 0:
            item_bombs.append(ItemBomb([100, random.randint(45, 400)], now, random.randint(2, 6)))
            timer_2 = 10000
        else:
            timer_2 -= 1
    # player
    player.update(now, keys)
    mouse_pos = pygame.mouse.get_pos()
    player.my_direction(mouse_pos)
    screen.blit(player.img, player.pos)
    # bomb
    i = 0
    while i < len(bombs):
        bombs[i].update(now)
        if bombs[i].position[0] < -64 or bombs[i].position[0] > 640 or bombs[i].position[1] < -64 or bombs[i].position[1] > 480:
            bombs.pop(i)
        else:
            bomb_img = pygame.transform.rotate(bombs[i].img, 360-bombs[i].direction*57.29)
            screen.blit(bomb_img, bombs[i].position)
            i += 1
    # bad guys
    j = 0
    while j < len(bad_guys):
        bad_guys[j].update(now, bad_guys)
        # collide
        i = 0
        while i < len(bombs):
            if bombs[i].boom_able and bad_guys[j].rect.colliderect(bombs[i].rect):
                bombs[i].boom(now, explodes, bombs)
                if bombs[i].number != 2:
                    bombs.pop(i)
                else:
                    i += 1
            else:
                i += 1
        if bad_guys[j].rect.left < 30 and now - bad_guys[j].attack_time > 3:
            health_val = bad_guys[j].attacking(health_val, now)
            if bad_guys[j].number == 10:
                bad_guys.pop(j)
            else:
                screen.blit(bad_guys[j].img, bad_guys[j].position)
                j += 1
        else:
            screen.blit(bad_guys[j].img, bad_guys[j].position)
            j += 1
    # explode
    i = 0
    while i < len(explodes):
        if explodes[i].atk_able:
            j = 0
            while j < len(bad_guys):
                if bad_guys[j].rect.colliderect(explodes[i].rect):
                    bad_guys[j].health -= explodes[i].attack
                    explodes[i].atk_able = False
                if bad_guys[j].health <= 0:
                    bad_guys[j].death(now, bad_guys, item_bombs)
                    bad_guys.pop(j)
                else:
                    if explodes[i].number == 3:
                        bad_guys[j].position[0] += 60
                    j += 1
        if now - explodes[i].set_time > explodes[i].sur_time:
            explodes.pop(i)
        else:
            screen.blit(explodes[i].img, explodes[i].position)
            i += 1
    # item_bomb
    i = 0
    while i < len(item_bombs):
        if now - item_bombs[i].set_time >= 8:
            item_bombs.pop(i)
        elif item_bombs[i].rect.colliderect(player.rect):
            player.pick_bomb(item_bombs[i].number, now)
            item_bombs.pop(i)
        else:
            screen.blit(item_bombs[i].img, item_bombs[i].position)
            i += 1
    # boss
    if is_bossing:
        boss.update(now, bad_guys)
        i = 0
        while i < len(bombs):
            if bombs[i].boom_able and boss.rect.colliderect(bombs[i].rect):
                bombs[i].boom(now, explodes, bombs)
                if bombs[i].number != 2:
                    bombs.pop(i)
                else:
                    i += 1
            else:
                i += 1
        i = 0
        while i < len(explodes):
            if explodes[i].atk_able_boss:
                if boss.rect.colliderect(explodes[i].rect):
                    boss.health -= explodes[i].attack
                    explodes[i].atk_able_boss = False
            i += 1
        if boss.number == 0 or boss.number == 1:
            screen.blit(boss.normal_img, boss.position)
        else:
            screen.blit(boss.angry_img, boss.position)

    # health and timer
    font = pygame.font.Font(None, 24)
    ti = pygame.time.get_ticks()
    if is_bossing:
        survived_text = font.render('boss health:' + str(boss.health), True, (0, 0, 0))
    else:
        survived_text = font.render(str((90000-pygame.time.get_ticks())//60000)+":" +
                                    str((90000-pygame.time.get_ticks())//1000 % 60).zfill(2), True, (0, 0, 0))
    text_rect = survived_text.get_rect()
    text_rect.topright = [635, 5]
    health_text = font.render(str(health_val), True, (0, 0, 0))
    text_rect_2 = health_text.get_rect()
    text_rect_2.topleft = [50, 40]
    screen.blit(image_from.heart_img, (0, 0))
    screen.blit(survived_text, text_rect)
    screen.blit(health_text, text_rect_2)
    # flash
    pygame.display.flip()
    # keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.set_bomb(bombs, now)

    if is_bossing and boss.health <= 0:
        running = False
        exitcode = True
    elif health_val <= 0:
        running = False
        exitcode = False

if exitcode:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    screen.blit(image_from.game_win_img, [80, 200])
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    screen.blit(image_from.game_over_img, [0, 0])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
