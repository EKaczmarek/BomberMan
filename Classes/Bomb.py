import pygame

class Bomb(object):
    def __init__(self, xx, yy):
        self.rect = pygame.Rect(xx, yy, 30, 30)

