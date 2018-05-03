import os
import pygame

class Button(object):
    mypath = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, picture, coords):
        self.image = pygame.image.load(os.path.join(self.mypath, picture))
        self.imagerect = self.image.get_rect()
        self.imagerect.topright = coords

    def show(self, surface):
        self.button = surface.blit(self.image, self.imagerect)

