import os.path
import pygame
import Classes.Wall as w
import Classes.Brick as b
import Classes.Button as btn
from Classes.Player_object import Player_object
from Classes.Bomb import Bomb
from Classes.Powerup import Powerup
import ast


class Board(object):
    level = None
    my_id = 0
    pos = None
    list_of_players = []
    screen = None
    images = []
    show_player = True
    rect = None

    def __init__(self):
        self.load_images()
        self.screen = None

        self.exitBtn = btn.Button(os.path.join("Pictures", "exit.png"), (200, 600))
        self.menuBtn = btn.Button(os.path.join("Pictures", "menu.png"), (400, 600))

        self.game = [[0 for col in range(15)] for row in range(15)]

        self.game_state = None

    def set_player_number(self, answer):
        for key, value in answer.items():
            # # print(type(key))
            if key.isdigit():
                # # print(key)
                self.my_id = key

    def set_map_level(self, map_level):
        print("w set map level...")
        print(map_level)
        lev = map_level
        self.level = map(''.join, zip(*[iter(lev)] * 15))

    def set_player_position(self, answer):
        x, y = (answer[self.my_id]["x"], answer[self.my_id]["y"])
        x_pixels, y_pixels = self.table_to_pixels(x, y)
        player_to_game = Player_object((x_pixels, y_pixels), self.my_id)
        self.game[y][x] = player_to_game.get_player()
        self.pos = x, y
        # print("player to same set player pos x y " + str(player_to_game.x) + " " + str(player_to_game.y))

    def set_list_of_players(self, answer):
        for key, value in answer["players"].items():
            x, y = value['x'], value['y']
            if str(key) != str(self.my_id):
                self.list_of_players.append({key: value})
                x_pixels, y_pixels = self.table_to_pixels(x, y)
                player_to_game = Player_object((x_pixels, y_pixels), key)
                self.game[y][x] = player_to_game.get_player()
                # print("list of players x y " + str(player_to_game.x) + " " + str(player_to_game.y))

    def handle_serwer_ans_on_get(self, answer_on_get):
        # I know it's dangerous but on windows json.loads doesnt work here :(
        answer = ast.literal_eval(answer_on_get)

        self.set_player_number(answer)
        self.set_map_level(answer["board"])
        self.set_player_position(answer)
        self.set_list_of_players(answer)

    def remove_player_from_map(self, json_dead):
        json_dead = ast.literal_eval(json_dead)

        if json_dead["PLAYERS_POS"] != {}:
            for k, v in json_dead["PLAYERS_POS"].items():
                x, y = v[0], v[1]
                self.game[x][y] = 0


        self.display_all()

    def show_efects_blow(self, json_bomb_blowing):

        json_bomb_blowing = ast.literal_eval(json_bomb_blowing)
        list_to_destroy = json_bomb_blowing["ELEMENTS_BLOW"]

        for i in list_to_destroy:
            for x in range(8):
                posx, posy = self.table_to_pixels(int(i[0]), int(i[1]))
                self.screen.blit(self.images[x], (posx, posy))
                pygame.display.flip()
            self.game[i[1]][i[0]] = 0

        self.show_board()



    def set_bomb_on_map(self, json_bombs):
        json_bombs = ast.literal_eval(json_bombs)
        x, y = json_bombs["BOMB_POS"]["x"], json_bombs["BOMB_POS"]["y"]

        x_pixels, y_pixels = self.table_to_pixels(x, y)
        bomb = Bomb(x_pixels, y_pixels, json_bombs["whose_bomb"])
        self.game[y][x] = bomb.get_bomb()

        self.show_board()


    def find_last_position(self, player_id):
        a, b = '', ''
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    player_desc = "player " + str(player_id)
                    if self.game[i][j].desc == player_desc:
                        # print(self.game[i][j].desc == player_desc)
                        return j, i
                    elif self.game[i][j].desc == "bomb":
                        if str(self.game[i][j].whose_bomb) == player_id:
                            a, b = j, i
        if a == '' and b == '':
            if player_id == 0:
                return 1, 1
            elif player_id == 1:
                return 13, 1
            elif player_id == 2:
                return 1, 13
            elif player_id == 3:
                return 13, 13
        else:
            return a, b

    # position nowa pozycja garcza w tablicy
    def update_player_position(self, player_id, position):
        # to do
        last_pos = self.find_last_position(player_id)
        if last_pos[1] != position["y"] or last_pos[0] != position["x"]:
            # print("position before change " + str(last_pos) + " desc " + str(self.game[last_pos[1]][last_pos[0]].desc))

            if self.game[last_pos[1]][last_pos[0]].desc == "bomb":
                 self.game[position["y"]][position["x"]] = Player_object(
                        (self.table_to_pixels(position["x"], position["y"])), player_id)
            else:
                self.game[position["y"]][position["x"]] = self.game[last_pos[1]][last_pos[0]]
                self.game[position["y"]][position["x"]].x, self.game[position["y"]][position["x"]].y = self.table_to_pixels(position["x"], position["y"])
                self.game[position["y"]][position["x"]].rect.x, self.game[position["y"]][position["x"]].rect.y = self.table_to_pixels(position["x"], position["y"])
                self.game[last_pos[1]][last_pos[0]] = 0

        self.show_board()

    def get_last_lost_bomb_by_player(self, player_id):
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == "bomb":
                        if self.game[i][j].whose_bomb == "player " + str(player_id):
                            last_player_bomb = i, j
        return last_player_bomb

    def get_player_position(self, player_id):
        player_desc = "player " + str(player_id)
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == player_desc:
                        # print(i, j)
                        return i, j
                    elif self.game[i][j].desc == "bomb":
                        if self.game[i][j].whose_bomb == player_id:
                            return i, j

    def init_map(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 750))
        self.screen.fill((255, 255, 255))
        pygame.mixer.music.load(r"Classes/Music/music.wav")

        # game board
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0

    def set_objects_on_map(self):
        self.walls_bricks()


    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def table_to_pixels(self, x, y):
        return int((x*50)+450), int(y*50)

    def walls_bricks(self):
        x = 450
        y = 0
        for row in self.level:
            for col in row:

                if col == "W":
                    wal = w.Wall((x, y))
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = wal.get_wall()

                elif col == "B":
                    brick = b.Brick((x, y))
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = brick.get_brick()

                elif col == "S" or col == "N" or col == "R":
                    powerup = Powerup((x, y), col)
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = powerup.get_powerup()

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

    def check_if_player_is_beside(self, i, j):
        # print(" w checck if player is beside ")
        table = [i, j + 1, i, j - 1, i - 1, j, i + 1, j]
        for k in range(0, 3):
            x = table[2 * k]
            y = table[2 * k + 1]
            if self.game[x][y] != 0:
                if self.game[x][y].desc[0:6] == "player":
                    return True
        return False

    def display_all(self):

        # Display screen
        wall = pygame.image.load(r"Classes/Pictures/wall.png").convert()
        box = pygame.image.load(r"Classes/Pictures/box.png").convert()
        bomba = pygame.image.load(r"Classes/Pictures/bomb.png")
        bomberman_left = pygame.image.load(r"Classes/Pictures/playerL.png").convert()
        bomberman_right = pygame.image.load(r"Classes/Pictures/playerR.png").convert()
        empty = pygame.image.load(r"Classes/Pictures/empty.png").convert()

        players_speed = pygame.image.load(r"Classes/Pictures/Background.png").convert()
        bombs_no = pygame.image.load(r"Classes/Pictures/obiekt.png").convert()
        bombs_range = pygame.image.load(r"Classes/Pictures/bomb.png").convert()


        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == "wall":
                        self.screen.blit(wall, self.game[i][j])
                    elif self.game[i][j].desc == "brick":
                        self.screen.blit(box, self.game[i][j])
                    elif self.game[i][j].desc[0:6] == "player":
                        self.screen.blit(bomberman_right, self.game[i][j])
                    elif self.game[i][j].desc == "bomb":
                        is_player_beside = self.check_if_player_is_beside(i, j)
                        if is_player_beside is True:
                            self.screen.blit(empty, self.game[i][j])
                        self.screen.blit(bomba, self.game[i][j])

                    elif self.game[i][j].desc == "powerup":
                        if self.game[i][j].kind == "S":
                            self.screen.blit(players_speed, self.game[i][j])
                        elif self.game[i][j].kind == "N":
                            self.screen.blit(bombs_no, self.game[i][j])
                        elif self.game[i][j].kind == "R":
                            self.screen.blit(bombs_no, self.game[i][j])

                else:
                    x, y = self.table_to_pixels(j, i)
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 50, 50))

        self.exitBtn.show(self.screen)
        self.menuBtn.show(self.screen)

        pygame.display.flip()
        pygame.display.update()

    def show_board(self):

        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    print(self.game[i][j].desc, end="\t")
                else:
                    print("\t", end="\t")
            print(end='\n')

        print("\n")



