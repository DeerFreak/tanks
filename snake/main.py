import pygame as pg
import time as t
from sprites import *
from settings import *
from os import path

class App(object):
    def __init__(self):
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.group_snake = pg.sprite.Group()
        self.group_Apple = pg.sprite.Group()
        self.snake = Snake(self)

    def draw(self):
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def app_running(self):
        self.game_running = True
        while self.game_running:
            self.all_sprites.update()
            self.draw()
    
    def events(self):
        pass

    def stscreen(self):
        pass

    def goscreen(self):
        pass


if __name__ == '__main__':
    snake = App()
    snake.stscreen()
    while snake.running:
        snake.new()
        snake.app_running()
        snake.goscreen()