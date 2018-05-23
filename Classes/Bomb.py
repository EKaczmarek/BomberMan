import pygame
import Classes.Board as board


class Bomb(object):

    def __init__(self, xx, yy):
        self.xx = xx
        self.yy = yy
        self.rect = pygame.Rect(self.xx, self.yy, 50, 50)
        self.start_timer = pygame.time.get_ticks()
        self.desc = "bomb"
        print(self.start_timer)

    def get_bomb(self):
        return self
