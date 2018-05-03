import pygame


class Brick(object):

    x, y = '', ''
    desc = "brick"

    def __init__(self, pos, bricks):
        self.x = pos[0]
        self.y = pos[1]
        bricks.append(self)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def get_brick(self):
        return self

