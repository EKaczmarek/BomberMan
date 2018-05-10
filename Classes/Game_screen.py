import Classes.Label as l
import Classes.InputBox as in_box
import Classes.Button as b
import Classes.Player as p
import pygame

class Game_screen:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 750))
        pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()

        self.buttons()

    def buttons(self):
        self.x_button_play, self.y_button_play = 600, 400
        self.varial = False
        self.done = False
        self.btn_play = b.Button('Pictures\PLAY.png', (self.x_button_play, self.y_button_play))

        self.x_button_ranking, self.y_button_ranking = 600, 200
        self.btn_ranking = b.Button('Pictures\RANKING.png', (self.x_button_ranking, self.y_button_ranking))

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.y_button_play <= mouse[1] <= self.y_button_play + 50 and self.x_button_play - 100 <= mouse[
                        0] <= self.x_button_play:
                            p.Player(500, 50)

            self.screen.fill((255, 255, 255))

            self.btn_ranking.show(self.screen)
            self.btn_play.show(self.screen)

            pygame.display.flip()
            self.clock.tick(30)