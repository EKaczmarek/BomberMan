import random
import pygame
import os
import Classes.Player as p
import Classes.Bomb as bom


def game():

    # Initialise pygame
    pygame.init()

    # Clock
    clock = pygame.time.Clock()


    # Create players
    player = p.Player(500, 50)
    player2 = p.Player(1100, 650)




if __name__ == "__main__":
    game()