import Classes.Label as l
import Classes.InputBox as in_box
import Classes.Button as b
import pygame

class Bad_data_screen:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 750))
        pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()

        self.labels()
        self.buttons()

    def labels(self):
        sign = l.Label(400, 500, "Pictures/sign_in.png")
        self.t0, self.t_rect0 = sign.getData()
        self.done = False

    def buttons(self):
        self.x_button_ok, self.y_button_ok = 600, 400
        self.varial = False
        self.btn = b.Button('Pictures\ok.png', (self.x_button_ok, self.y_button_ok))

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.y_button_ok <= mouse[1] <= self.y_button_ok + 50 and self.x_button_ok - 100 <= mouse[
                        0] <= self.x_button_ok:
                                print("eKRAN 2")

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.t0, self.t_rect0)
            self.btn.show(self.screen)

            pygame.display.flip()
            self.clock.tick(30)