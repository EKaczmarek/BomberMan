import pygame

class Wall(object):

    def __init__(self, pos, walls):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)
