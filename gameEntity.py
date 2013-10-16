# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame

SCREEN_WIDTH = 390
SCREEN_HEIGHT = 650

PLAYER_WIDTH = 102
PLAYER_HEIGHT = 126

ENEMY_SMALL = 1
ENEMY_MIDDLE = 2
ENEMY_BIG = 3

ENEMY_SAMLL_SPEED = 3
ENEMY_MIDDLE_SPEED = 2
ENEMY_BIG_SPEED = 1

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家对象精灵图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家精灵图片索引
        self.is_hit = False                             # 玩家是否被击中

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

# 敌人类
class _Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs

    def move(self):
        self.rect.top += self.speed
    
    # 判断是否被子弹击落    
    def isDown(self):
        return self.shootcount == 0

class Enemy_Small(_Enemy): 
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):  
        _Enemy.__init__(self, enemy_img, enemy_down_imgs, init_pos) 
        self.speed = ENEMY_SAMLL_SPEED
        self.shootcount = 1
        self.score = 1000
        self.down_index = 0
        
class Enemy_Middle(_Enemy): 
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):  
        _Enemy.__init__(self, enemy_img, enemy_down_imgs, init_pos) 
        self.speed = ENEMY_MIDDLE_SPEED
        self.shootcount = 2
        self.score = 2000
        self.down_index = 0
        
class Enemy_Big(_Enemy): 
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):  
        _Enemy.__init__(self, enemy_img, enemy_down_imgs, init_pos) 
        self.speed = ENEMY_BIG_SPEED    
        self.shootcount = 5  
        self.score = 5000
        self.down_index = 0      