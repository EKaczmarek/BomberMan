import pygame
import time

class Player_object_board(object):
    x, y = '', ''
    desc = ''
    bombs = ''
    speed = ''
    range_bomb = ''

    def __init__(self, pos, player, bombs, range, speed):
        self.x = pos[0]
        self.y = pos[1]
        self.desc = player
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.bombs = bombs
        self.range_bomb = range
        self.speed = speed

    def set_bombs_number(self):
        self.bombs = 2

    def start_timer(self):
        time.sleep(3)
        self.reset_bombs_number()
        print("Reset bombs number")

    def set_speed(self):
        self.speed = 2

    def set_range_bomb(self):
        self.range_bomb = 2

    def reset_bombs_number(self):
        self.bombs = 1

    def reset_speed(self):
        self.speed = 1

    def reset_range_bombs(self):
        self.range_bomb = 1

    def get_player(self):
        return self
