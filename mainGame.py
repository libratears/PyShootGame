# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
# 导入一些常用的变量和函数
from pygame.locals import *
from gameEntity import *
import random

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('飞机大战')

# 载入游戏音乐
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
bullet_sound.set_volume(0.25)
enemy_small_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
enemy_small_down_sound.set_volume(0.3)
enemy_middle_down_sound = pygame.mixer.Sound('resources/sound/enemy2_down.wav')
enemy_middle_down_sound.set_volume(0.3)
enemy_big_down_sound = pygame.mixer.Sound('resources/sound/enemy3_down.wav')
enemy_big_down_sound.set_volume(0.3)
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.2)

# 载入背景图
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 设置玩家相关参数
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))

player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [(SCREEN_WIDTH - PLAYER_WIDTH) /2, SCREEN_HEIGHT - PLAYER_HEIGHT]      # 玩家初始位置
player = Player(plane_img, player_rect, player_pos)

# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义小型敌机对象使用的surface相关参数
enemy_small_rect = pygame.Rect(534, 612, 57, 43)
enemy_small_img = plane_img.subsurface(enemy_small_rect)
# 小型敌机被击中精灵图片
enemy_small_down_imgs = []
enemy_small_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_small_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_small_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_small_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

# 定义中型敌机对象使用的surface相关参数
enemy_middle_rect = pygame.Rect(0 ,0, 69, 99)
enemy_middle_img = plane_img.subsurface(enemy_middle_rect)
# 中型敌机被击中精灵图片
enemy_middle_down_imgs = []
enemy_middle_down_imgs.append(plane_img.subsurface(pygame.Rect(534, 655, 69, 99)))
enemy_middle_down_imgs.append(plane_img.subsurface(pygame.Rect(603, 655, 69, 99)))
enemy_middle_down_imgs.append(plane_img.subsurface(pygame.Rect(672, 653, 69, 99)))
enemy_middle_down_imgs.append(plane_img.subsurface(pygame.Rect(741, 653, 69, 99)))

# 定义大型敌机对象使用的surface相关参数
enemy_big_rect = pygame.Rect(504, 750, 165, 261)
enemy_big_img = plane_img.subsurface(enemy_big_rect)
# 大型敌机被击中精灵图片
enemy_big_down_imgs = []
enemy_big_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 486, 165, 261)))
enemy_big_down_imgs.append(plane_img.subsurface(pygame.Rect(839, 748, 165, 261)))
enemy_big_down_imgs.append(plane_img.subsurface(pygame.Rect(673, 748, 165, 261)))
enemy_big_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 747, 165, 261)))

enemies = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁精灵动画
enemies_down = pygame.sprite.Group()

shoot_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True

while running:
    # 控制游戏最大帧率为60
    clock.tick(60)

    # 控制发射子弹频率,并发射子弹
    if not player.is_hit:
        if shoot_frequency % 10 == 0:
            bullet_sound.play()
            player.shoot(bullet_img)
            shoot_frequency = 0
        shoot_frequency += 1

    # 生成敌机
    rint = random.randint(1, 500)
    if rint % 30 == 0:
        enemy_small_pos = [random.randint(0, SCREEN_WIDTH - enemy_small_rect.width), 0]
        enemy_small = Enemy_Small(enemy_small_img, enemy_small_down_imgs, enemy_small_pos)
        enemies.add(enemy_small)
    elif rint % 80 == 0:
        enemy_middle_pos = [random.randint(0, SCREEN_WIDTH - enemy_middle_rect.width), 0]
        enemy_middle = Enemy_Middle(enemy_middle_img, enemy_middle_down_imgs, enemy_middle_pos)
        enemies.add(enemy_middle)
    elif rint % 250 == 0:
        enemy_big_pos = [random.randint(0, SCREEN_WIDTH - enemy_big_rect.width), 0]
        enemy_big = Enemy_Big(enemy_big_img, enemy_big_down_imgs, enemy_big_pos)
        enemies.add(enemy_big)

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top < 0:
            enemies.remove(enemy)

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies_shooted = pygame.sprite.groupcollide(enemies, player.bullets, 0, 1)
    for enemy_down in enemies_shooted:
        enemy_down.shootcount = enemy_down.shootcount - 1
        if enemy_down.isDown():
            enemies_down.add(enemy_down)
            enemies.remove(enemy_down)

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency / 8
    else:
        player.img_index = player_down_index / 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            if type(enemy_down) == Enemy_Small:
                enemy_small_down_sound.play()
            elif type(enemy_down) == Enemy_Middle:
                enemy_middle_down_sound.play()
            elif type(enemy_down) == Enemy_Big:
                enemy_big_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += enemy_down.score
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index / 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies.draw(screen)

    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # 监听键盘事件
    key_pressed = pygame.key.get_pressed()
    # 若玩家被击中，则无效
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

# 游戏结束，显示总得分
font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()