import pygame


class Wall(object):

    x, y = '', ''
    desc = "wall"

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)

    def get_wall(self):
        return self
