import pygame


class Player_object_board(object):
    x, y = '', ''
    desc = ''
    def __init__(self, pos, player):
        self.x = pos[0]
        self.y = pos[1]
        self.desc = player
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def get_player(self):
        return self
