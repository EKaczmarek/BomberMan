import pygame
import Classes.Board as board
import Classes.Bomb as bom


class Player(object):

    walls = []  # List to hold walls
    bricks = []  # List to hold bricks

    def __init__(self, x, y):
        # Initialise pygame
        self.pygame = pygame.init()

        self.rect = pygame.Rect(x, y, 50, 50)
        self.board = board.Board(self.walls, self.bricks)

        self.show_player = False
        self.exit_key = False
        self.bomb_key = False
        self.left_bombs = 0

        self.main_loop()

    def main_loop(self):
        while (self.exit_key != True):
            self.show_player = True
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
            if (seconds >= 1):
                self.bomb.blow()
                self.bomb_key = False
                print(self.left_bombs)

    def display_all(self):
        # Display screen
        self.board.screen.fill((255, 255, 255))

        # Display bricks
        for brick in self.bricks:
            pygame.draw.rect(self.board.screen, (255, 100, 50), brick.rect)

        # Display walls
        for wall in self.walls:
            pygame.draw.rect(self.board.screen, (0, 0, 0), wall.rect)
            if (self.show_player):
                pygame.draw.rect(self.board.screen, (255, 200, 0), self.rect)
            if (self.bomb_key):
                pygame.draw.rect(self.board.screen, (255, 0, 255), self.bomb.rect)

        # Display buttons
        self.board.exitBtn.show(self.board.screen)
        self.board.menuBtn.show(self.board.screen)

        pygame.display.flip()

    def leave_bomb(self):
        if (self.bomb_key == False):
            xx, yy = self.get_pos()
            self.bomb = bom.Bomb(xx, yy)
            self.left_bombs += 1
            self.bomb_key = True

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in self.walls:
            print(self.rect.x, '', self.rect.y)
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

        for brick in self.bricks:
            #print(self.rect.x, '', self.rect.y)
            if self.rect.colliderect(brick.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = brick.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = brick.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = brick.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = brick.rect.bottom

    def get_pos(self):
        return self.rect.x, self.rect.y

