import pygame


class Brick(object):

    x, y = '', ''
    desc = "brick"
    # box = pygame.image.load(r"C:/Users/Mario/Documents/GitHub/BomberMan/Classes/Pictures/box.png")
    # box = pygame.image.load(r"Classes/Pictures/box.png")

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        # self.rect = self.box.get_rect()

    def get_brick(self):
        return self


