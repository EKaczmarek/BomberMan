import pygame


class Powerup(object):

    x, y = '', ''

    desc = "powerup"

    # kind of powerups:
        # speed of moving player    ==> player_speed        ==> S
        # number of bombs           ==> bombs_no            ==> N
        # range of bomb             ==> bombs_range         ==> R
    kind = ''

    # view will be changed from brick to powerup when on view should be not brick but powerup
    view = "brick"

    def __init__(self, pos, kind):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.kind = kind

    def change_view(self, view):
        self.view = view

    def get_powerup(self):
        return self