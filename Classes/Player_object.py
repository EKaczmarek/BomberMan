import pygame

class Player_object(object):

    x, y = '', ''
    desc = "player"

    def __init__(self, pos, id):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.desc = "player " + id

    def get_player(self):
        return self




