#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys

DEFAULT_DISPLAY_SIZE=(640,480)

class Point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y



def init():
    pygame.init()
    screen = pygame.display.set_mode(DEFAULT_DISPLAY_SIZE,pygame.RESIZABLE)                # 大きさ600*500の画面を生成
    pygame.display.set_caption("幾何")
    return screen


def main():
    screen = init()

    while (True):
        screen.fill((0,0,0))                                    # 画面を黒色に塗りつぶし
        pygame.display.update()                                 # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:                              # 閉じるボタンが押されたら終了
                pygame.quit()                                   # Pygameの終了(画面閉じられる)
                sys.exit()
            if event.type == VIDEORESIZE:
                # The main code that resizes the window:
                # (recreate the window with the new size)
                screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
                print("w={} h={}".format(event.w,event.h))

if __name__=='__main__':main()