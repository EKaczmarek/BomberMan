import pygame
import Classes.Board as board
import Classes.Bomb as bom

class Player(object):

    walls = []  # List to hold walls
    bricks = []  # List to hold bricks

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.board = board.Board(self.walls, self.bricks)

        # Set up the display
        screen = pygame.display.set_mode((1200, 750))

        varial = False
        running = True
        bomb_key = False

        while running:
            #clock.tick(60)
            for e in pygame.event.get():
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
                        xx, yy = self.getPos()
                        bomb = bom.Bomb(xx, yy)
                        bomb_key = True

                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if (self.board.exitBtn.button.collidepoint(mouse)):
                        running = False
                    if (self.board.menuBtn.button.collidepoint(mouse)):
                        varial = True

            # Wyświetlenie tła, ścian, zawodnika
            screen.fill((255, 255, 255))
            for brick in self.bricks:
                pygame.draw.rect(screen, (255, 100, 50), brick.rect)
            for wall in self.walls:
                pygame.draw.rect(screen, (0, 0, 0), wall.rect)
                if (varial):
                    pygame.draw.rect(screen, (255, 200, 0), self.rect)
                if (bomb_key):
                    pygame.draw.rect(screen, (255, 0, 255), bomb.rect)

            self.board.exitBtn.show(screen)
            self.board.menuBtn.show(screen)
            pygame.display.flip()


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

    def getPos(self):
        return self.rect.x, self.rect.y

