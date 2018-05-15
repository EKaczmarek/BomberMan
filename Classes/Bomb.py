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
        self.images = pygame.image.load(r"Classes/Pictures/explosion.png").convert()
        self.numImages = 11
        self.cImage = 0


    def blow(self):
        print("Wybuchaa!!!")
        if (self.cImage >= self.numImages-1):

            self.cImage = 0
        else:

            self.cImage += 1

    def get_bomb(self):
        return self
