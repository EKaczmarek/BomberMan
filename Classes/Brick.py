import pygame

class Brick(object):
    def __init__(self, pos, bricks):
        bricks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)
