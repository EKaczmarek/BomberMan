import pygame


class Bomb(object):

    desc = "BOMB"

    def __init__(self, xx, yy):
        self.xx = xx
        self.yy = yy
        self.rect = pygame.Rect(self.xx, self.yy, 50, 50)
        self.start_timer = pygame.time.get_ticks()
        print(self.start_timer)

    def blow(self):
        print("Wybuchaa!!!")

    def get_bomb(self):
        return self
