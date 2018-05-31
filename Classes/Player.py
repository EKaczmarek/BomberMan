import pygame
import time
import glob
import Classes.Board as board
import Classes.Bomb as bom
import Classes.Wall as wal
import Classes.Brick as brick
import Classes.Powerup as powerup
import re


def load_image(name):
    image = pygame.image.load(name)
    return image


class Player(object):

    walls = []  # List to hold walls
    bricks = []  # List to hold bricks
    side = 0

    lista = []
    images = []

    def __init__(self, parent = None):
        # Initialise pygame
        self.pygame = pygame.init()
        # Position of player
        #self.rect = pygame.Rect(x, y, 50, 50)

        self.load_images()
        # Initialize board, get info about position from server
        self.board = board.Board()
        # set position of player from server
        self.set_player_pos()
        self.rect = pygame.Rect(self.x_px, self.y_px, 50, 50)

        # Initialize flags
        self.show_player = True
        self.exit_key = False
        self.bomb_key = False
        self.left_bombs = 0
        # Main loop
        self.main_loop()
        #client to sending message to server

    def set_player_pos(self):
        print("Pozycja gracza od serwera: " + self.board.player_pos)
        y = int(re.search('x(.*)y', self.board.player_pos).group(1))
        x = int(re.search('y(.*)', self.board.player_pos).group(1))
        x_px, y_px = self.board.table_to_pixels(x, y)
        print("Pikselowo: " + str(y_px) + " " + str(x_px))
        self.x_px = y_px
        self.y_px = x_px


    def load_images(self):
        self.images.append(load_image(r"Classes/Pictures/ex1.png"))
        self.images.append(load_image(r"Classes/Pictures/ex2.png"))
        self.images.append(load_image(r"Classes/Pictures/ex3.png"))
        self.images.append(load_image(r"Classes/Pictures/ex4.png"))
        self.images.append(load_image(r"Classes/Pictures/ex5.png"))
        self.images.append(load_image(r"Classes/Pictures/ex6.png"))
        self.images.append(load_image(r"Classes/Pictures/ex7.png"))
        self.images.append(load_image(r"Classes/Pictures/ex8.png"))

        images_right = self.images
        images_left = [pygame.transform.flip(image, True, False) for image in self.images]  # Flipping every image.
        index = 0
        image = self.images[index]

    def main_loop(self):
        while (self.exit_key != True):
            self.handle_moves()
            self.handle_bombs()
            self.display_all()

    def handle_moves(self):

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.move(-50, 0)
                    Player.side = 1
                if e.key == pygame.K_RIGHT:
                    self.move(50, 0)
                    Player.side = 0
                if e.key == pygame.K_UP:
                    self.move(0, -50)
                if e.key == pygame.K_DOWN:
                    self.move(0, 50)
                if e.key == pygame.K_b:
                    self.leave_bomb()

            # actions = clickig Exit, Menu
            if e.type == pygame.QUIT:
                self.exit_key = True
                self.send_message_to_server("EXIT")
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.exit_key = True
                self.send_message_to_server("EXIT")
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.mouse.get_pos()
                if (self.board.exitBtn.button.collidepoint(mouse)):
                    self.send_message_to_server("EXIT")
                    self.exit_key = True

    def send_message_to_server(self, message):
        self.board.cl.sendMessage(message)

    def check_is_player_dead(self):
        message = "D "
        self.send_message_to_server(message)
        answer = self.board.cl.wait4Response()
        print("Odpowiedzialalalal " +  answer)
        if (answer == "True"): return True
        else: return False


    def handle_bombs(self):
        powUP = pygame.image.load(r"Classes/Pictures/wall.png").convert()
        if (self.bomb_key == True):
            seconds = (pygame.time.get_ticks() - self.bomb.start_timer) / 1000
            if (seconds >= 1.5):
                self.bomb_key = False
                ans = self.check_is_player_dead()
                for i in self.board.list_to_destroy:
                    for x in range(8):
                        posx, posy = self.board.table_to_pixels(int(i[0]), int(i[1]))
                        self.board.screen.blit(self.images[x], (posy, posx))
                        pygame.display.flip()
                    self.board.game[i[0]][i[1]] = 0
                if (ans):
                    self.show_player = False

    def display_all(self):
        # Display screen
        wall = pygame.image.load(r"Classes/Pictures/wall.png").convert()
        box = pygame.image.load(r"Classes/Pictures/box.png").convert()
        bomba = pygame.image.load(r"Classes/Pictures/bomb.png")
        bombermanL = pygame.image.load(r"Classes/Pictures/playerL.png").convert()
        bombermanR = pygame.image.load(r"Classes/Pictures/playerR.png").convert()

        self.board.screen.fill((255, 255, 255))

        for i in range(len(self.board.game)):
            for j in range(len(self.board.game[i])):
                if(self.board.game[i][j] != 0):
                    if(self.board.game[i][j].desc == "wall"):
                        self.board.screen.blit(wall, self.board.game[i][j])
                        if (self.show_player):
                            if(Player.side == 0):
                                self.board.screen.blit(bombermanR, self.rect)
                            else:
                                self.board.screen.blit(bombermanL, self.rect)
                        if (self.bomb_key):
                            self.board.screen.blit(bomba, self.bomb.rect)
                    elif(self.board.game[i][j].desc == "brick"):
                        self.board.screen.blit(box, self.board.game[i][j])
                else:
                    pygame.draw.rect(self.board.screen, (255, 255, 255), self.rect)

        self.board.exitBtn.show(self.board.screen)
        self.board.menuBtn.show(self.board.screen)

        pygame.display.flip()

    def send_to_server_info_bomb(self):
        self.board.list_to_destroy = []
        print("Aktualna pozycja bomby x:" + str(self.get_pos()[0]) + " y:" + str(self.get_pos()[1]))
        message = "B x" + str(self.get_pos()[0]) + "y" + str(self.get_pos()[1])
        self.send_message_to_server(message)
        print("do serwera wyslano :" + message)
        a = self.board.cl.wait4Response()
        print("Serwer odpowiedzial: ")

        for i in a:
            print("Element " + str(i[0]) + " " + str(i[1]))
            self.board.list_to_destroy.append((i[0], i[1]))

    def leave_bomb(self):
        BombExplode = pygame.mixer.Sound('Classes/Music/TimeBomb.wav')
        if (self.bomb_key == False):
            xx, yy = self.get_pos_to_bomb()
            print("xx " + str(xx) + " yy " + str(yy))

            self.send_to_server_info_bomb()
            self.bomb = bom.Bomb(xx, yy)

            self.left_bombs += 1

            self.board.game[int(yy / 50)][int((xx - 450) / 50)] = self.bomb.get_bomb()
            self.bomb_key = True

            pygame.mixer.Sound.play(BombExplode)

            print(self.board.list_to_destroy)



    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for i in range(len(self.board.game)):
            for j in range(len(self.board.game[i])):
                if((type(self.board.game[i][j]) is wal.Wall)
                   or (type(self.board.game[i][j]) is brick.Brick)
                   or (type(self.board.game[i][j]) is bom.Bomb)):
                    if self.rect.colliderect(self.board.game[i][j].rect):
                        if dx > 0:  # Moving right; Hit the left side of the wall
                            self.rect.right = self.board.game[i][j].rect.left
                        if dx < 0:  # Moving left; Hit the right side of the wall
                            self.rect.left = self.board.game[i][j].rect.right
                        if dy > 0:  # Moving down; Hit the top side of the wall
                            self.rect.bottom = self.board.game[i][j].rect.top
                        if dy < 0:  # Moving up; Hit the bottom side of the wall
                            self.rect.top = self.board.game[i][j].rect.bottom

        print("ASktualna pozycja x:" + str(self.get_pos()[0]) + " y:" + str(self.get_pos()[1]))
        message = "P x" + str(self.get_pos()[0]) + "y" + str(self.get_pos()[1])
        self.send_message_to_server(message)
        print("do serwera wyslano :" + message)
        self.board.cl.wait4Response()

    def get_pos(self):
        print("Wspolrzedne 1: ", self.rect.x, ", ",self.rect.y)
        xx = int((self.rect.x - 450) / 50)
        yy = int(self.rect.y / 50)
        print("Wspolrzedne 2: ", xx, ", ", yy)
        return xx, yy

    def get_pos_to_bomb(self):
        return self.rect.x, self.rect.y