import pygame


class Powerup(object):

    x, y = '', ''
    desc = "powerup"

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def get_powerup(self):
        return self