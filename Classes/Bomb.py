import pygame


class Bomb(object):

    desc = "bomb"
    whose_bomb = ""

    def __init__(self, x, y, whose_bomb):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.whose_bomb = whose_bomb

        # self.start_timer = pygame.time.get_ticks()
        # print(self.start_timer)

    def get_bomb(self):
        return self
