import pygame
import Classes.Board as board
import Classes.Bomb as bom
import Classes.Wall as wal
import Classes.Brick as brick


class Player(object):

    walls = []  # List to hold walls
    bricks = []  # List to hold bricks

    def __init__(self, x, y):
        # Initialise pygame
        self.pygame = pygame.init()
        # Position of player
        self.rect = pygame.Rect(x, y, 50, 50)
        # Initialize board
        self.board = board.Board(self.walls, self.bricks)
        # Initialize flags
        self.show_player = True
        self.exit_key = False
        self.bomb_key = False
        self.left_bombs = 0
        # Main loop
        self.main_loop()

    def main_loop(self):
        while (self.exit_key != True):
            self.handle_moves()
            self.handle_bombs()
            self.display_all()

    def handle_moves(self):

        for e in pygame.event.get():
            # buttons
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.move(-50, 0)
                if e.key == pygame.K_RIGHT:
                    self.move(50, 0)
                if e.key == pygame.K_UP:
                    self.move(0, -50)
                if e.key == pygame.K_DOWN:
                    self.move(0, 50)
                if e.key == pygame.K_b:
                    self.leave_bomb()

            # actions = clickig Exit, Menu
            if e.type == pygame.QUIT:
                self.exit_key = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.exit_key = True
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.mouse.get_pos()
                if (self.board.exitBtn.button.collidepoint(mouse)):
                    self.exit_key = True

    def handle_bombs(self):
        # bomb timer
        if (self.bomb_key == True):
            seconds = (pygame.time.get_ticks() - self.bomb.start_timer) / 1000
            if (seconds >= 2):
                self.bomb.blow()
                self.bomb_key = False
                print(self.to_destroy)


                self.to_destroy.append((self.get_changed_pos(self.bomb.xx, self.bomb.yy)))
                print("Lista: ", self.to_destroy)
                for i in self.to_destroy:
                    print(i)
                    self.board.game[i[0]][i[1]] = 0
                print("Bomba: ", self.bomb.xx, " ", self.bomb.yy)

                ans = self.destroy_player(self.bomb.xx, self.bomb.yy)
                print(ans)
                if (ans):
                    self.die()

    def die(self):
        self.show_player = False

    def display_all(self):
        # Display screen
        self.board.screen.fill((255, 255, 255))

        for i in range(len(self.board.game)):
            for j in range(len(self.board.game[i])):
                if(self.board.game[i][j] != 0):
                    if(self.board.game[i][j].desc == "wall"):
                        pygame.draw.rect(self.board.screen, (0, 0, 0), self.board.game[i][j].rect)
                        if (self.show_player):
                            pygame.draw.rect(self.board.screen, (255, 200, 0), self.rect)
                        if (self.bomb_key):
                            pygame.draw.rect(self.board.screen, (255, 0, 255), self.bomb.rect)
                    elif(self.board.game[i][j].desc == "brick"):
                        pygame.draw.rect(self.board.screen, (255, 100, 50), self.board.game[i][j].rect)
                        # Display buttons
                else:
                    pygame.draw.rect(self.board.screen, (255, 255, 255), self.rect)

        self.board.exitBtn.show(self.board.screen)
        self.board.menuBtn.show(self.board.screen)

        pygame.display.flip()

    def leave_bomb(self):
        if (self.bomb_key == False):


            xx, yy = self.get_pos_to_bomb()

            self.bomb = bom.Bomb(xx, yy)
            print("lolaola: ", xx, " ", yy)

            self.board.game[int(yy / 50)][int((xx - 450) / 50)] = self.bomb.get_bomb()

            self.left_bombs += 1
            self.bomb_key = True

            # Count which bricks explode
            self.to_destroy = self.board.count(xx, yy)
            # Count if player will be dead
            destroy_player = self.destroy_player(xx, yy)

            print(destroy_player)

            if(destroy_player != 0):
                self.to_destroy.append(destroy_player)
            print(self.to_destroy)

    def destroy_player(self, xx, yy):

        x, y = self.get_pos()
        print("Player", x, " ", y)
        xx = int((xx - 450) / 50)
        yy = int(yy / 50)
        print("Bomba 1: ", xx, " ", yy)
        if((x == xx and y == yy)
           or (x == xx+1 and y == yy)
           or (x == xx-1 and y == yy)
           or (x == xx and y == yy+1)
           or (x == xx and y == yy-1)):
            print("gracz:", x, " ", y)
            return (y, x)
        else:
            return 0

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

    def get_pos(self):
        print("Wspolrzedne1: ", self.rect.x, ", ",self.rect.y)
        xx = int((self.rect.x - 450) / 50)
        yy = int(self.rect.y / 50)
        print("Wspolrzedne2: ", xx, ", ", yy)
        return xx, yy

    def get_changed_pos(self, xx, yy):
        xx = int((xx - 450) / 50)
        yy = int(yy / 50)
        return xx, yy

    def get_pos_to_bomb(self):
        return self.rect.x, self.rect.y