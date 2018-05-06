import pygame

class Wall(object):

    x, y = '', ''
    desc = "wall"

    def __init__(self, pos, walls):
        self.x = pos[0]
        self.y = pos[1]
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)

    def get_wall(self):
        return self

    def change_xy(self, x, y):
        return int(y / 50), int((x - 450) / 50)

    def get_pos_wall(self):
        return self.x, self.y