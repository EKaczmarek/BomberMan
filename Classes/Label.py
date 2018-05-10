import pygame
import os

class Label:
    mypath = os.path.dirname(os.path.realpath(__file__))

    def __init__(self,x,y, obraz):
        self.t1 = pygame.image.load(os.path.join(self.mypath, obraz))
        self.t_rect1 = self.t1.get_rect()
        self.t_rect1.centerx, self.t_rect1.centery = x,y


    def getData(self):
        return self.t1, self.t_rect1