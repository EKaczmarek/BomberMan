import os.path
import pygame
import Classes.Wall as w
import Classes.Brick as b
import Classes.Powerup as p
import Classes.Button as btn
from Classes.Player_object import Player_object
import ast

class Board(object):
    level = [
            "WWWWWWWWWWWWWWW",
            "W    BBBBBBB  W",
            "WBW W W W W W W",
            "WB  B   BBB   W",
            "WBW WBW W W W W",
            "W   BBBBBBBB  W",
            "W W W W W W W W",
            "W  BB         W",
            "W W W W W W W W",
            "W BBBBBBBBBB  W",
            "W W W WBWBW W W",
            "WB  BBBBBB    W",
            "WBW W WBW W W W",
            "WBB B  B      W",
            "WWWWWWWWWWWWWWW",
        ]

    my_id = 0
    pos = None
    list_of_players = []
    screen = None
    images = []
    show_player = True
    rect = None

    def __init__(self):
        print("Init map")
        self.load_images()

        self.screen = None

        print("po screen.init ")


        self.exitBtn = btn.Button(os.path.join("Pictures", "exit.png"), (200, 600))
        self.menuBtn = btn.Button(os.path.join("Pictures", "menu.png"), (400, 600))

        self.powerups_array = [[0 for columns in range(15)] for rows in range(15)]

        self.game = [[0 for col in range(15)] for row in range(15)]


        # Set up the display

    def set_player_number(self, answer):
        for key, value in answer.items():
            print(type(key))
            if key.isdigit():
                print(key)
                self.my_id = key

    def set_map_level(self, map_level):
        level = map_level
        self.level = map(''.join, zip(*[iter(level)] * 15))

    def set_player_position(self, answer):
        self.pos = (answer[self.my_id]["x"], answer[self.my_id]["y"])
        player_to_game = Player_object((self.table_to_pixels(self.pos[0], self.pos[1])), self.my_id)
        print("self.pos ", self.pos)
        print("player_to_game.x ", player_to_game.x)
        print("player_to_game.y ", player_to_game.y)
        print("player_to_game.desc ", player_to_game.desc)
        self.game[self.pos[0]][self.pos[1]] = player_to_game.get_player()

    def set_list_of_players(self, answer):
        print("Inni gracze:")
        for key, value in answer.items():
            if key == "players":
                for k, v in value.items():
                    if str(k) != str(self.my_id):
                        self.list_of_players.append({k: v})
                        print("k: ", k)
                        print("v: ", v)

    def handle_serwer_ans_on_get(self, answer_on_get):
        # I know it's dangerous but on windows json.loads doesnt work here :(
        answer = ast.literal_eval(answer_on_get)

        self.set_player_number(answer)
        self.set_map_level(answer["board"])
        self.set_player_position(answer)
        self.set_list_of_players(answer)

        print("..... KONIEC PRZETWARZANIA ODPOWIEDZI SERWERA NA GET .....")
        print("..... Plansza: ", self.level)
        print("..... Moja pozycja: ", self.pos)
        print("..... Inni gracze: " + str(self.list_of_players))

    def init_map(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 750))
        self.screen.fill((255, 255, 255))
        pygame.mixer.music.load(r"Classes/Music/music.wav")

        """print("Moje dane caly czas te same")
        print("self.other_players ", self.list_of_players)
        print("self.pos[0] ", self.pos[0])
        print("self.pos[1] ", self.pos[1])"""

        # Powerups
        for i in range(len(self.powerups_array)):
            for j in range(len(self.powerups_array[i])):
                self.powerups_array[i][j] = 0

        # game board
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0
            print()

        # TO DO
        # dla pozostalych graczy na liscie

        print(" po init map")

    def set_objects_on_map(self):
        self.walls_bricks()

    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def table_to_pixels(self, x, y):
        return int((y*50)+450), int(x*50)

    def walls_bricks(self):
        x = 450
        y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    wal = w.Wall((x, y))
                    # x is a multiply of 50 f.ex 450, y also
                    # so it's easier to have element table[1][1] than table[50][50] etc
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = wal.get_wall()
                elif col == "B":
                        brick = b.Brick((x, y))
                        #powerUP = p.Powerup((x, y))
                        table_x, table_y = self.table_dimension(y, x)
                        self.game[table_x][table_y] = brick.get_brick()
                        # rand = random.randint(0, 100)
                        # if (rand > 0):

                        # table_x, table_y = self.table_dimension(y, x)
                        # self.powerups_array[table_x][table_y] = powerUP.get_powerup()
                x += 50
            y += 50
            x = 450

    def load_images(self):
        self.images.append(self.load_image(r"Classes/Pictures/ex1.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex2.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex3.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex4.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex5.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex6.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex7.png"))
        self.images.append(self.load_image(r"Classes/Pictures/ex8.png"))

        images_right = self.images
        images_left = [pygame.transform.flip(image, True, False) for image in self.images]  # Flipping every image.
        index = 0
        image = self.images[index]

    def load_image(self, name):
        image = pygame.image.load(name)
        return image

    def display_all(self):
        # Display screen
        wall = pygame.image.load(r"Classes/Pictures/wall.png").convert()
        box = pygame.image.load(r"Classes/Pictures/box.png").convert()
        bomba = pygame.image.load(r"Classes/Pictures/bomb.png")
        bombermanL = pygame.image.load(r"Classes/Pictures/playerL.png").convert()
        bombermanR = pygame.image.load(r"Classes/Pictures/playerR.png").convert()
        empty = pygame.image.load(r"Classes/Pictures/empty.png").convert()

        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == "wall":
                        self.screen.blit(wall, self.game[i][j])
                        #if self.show_player:

                        """for item in self.list_of_players:
                            print("item ", item)
                            for k, v in item.items():
                                print("k ", k)
                                print("v ", v)
                                self.screen.blit(bombermanR, self.game[i][j].get_player)
                                print("W display_all")
                                print(item)"""

                            #  if (Player.side == 0):
                            # self.screen.blit(bombermanR, self.rect)
                            # else:
                            #    self.board.screen.blit(bombermanL, self.rect)
                        # if (self.bomb_key):
                            # self.board.screen.blit(bomba, self.bomb.rect)
                    elif self.game[i][j].desc == "brick":
                        self.screen.blit(box, self.game[i][j])
                    elif self.game[i][j].desc[0:6] == "player":
                        self.screen.blit(bombermanR, self.game[i][j])
                """else:
                    pygame.draw.rect(self.screen, (255, 255, 255), player_rect)"""

        self.exitBtn.show(self.screen)
        self.menuBtn.show(self.screen)

        pygame.display.flip()

    def show_board(self):
        a = self.game
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    print(self.game[i][j].x, " ", self.game[i][j].y, " ", self.game[i][j].desc, end='\n')
            print()



