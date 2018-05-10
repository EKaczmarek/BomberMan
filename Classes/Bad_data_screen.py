import Classes.Player as pl
import Classes.Label as l
import Classes.InputBox as in_box
import Classes.Button as b
import os
import pygame

class Bad_data_screen:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 750))
        pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()

        self.inputs()
        self.labels()
        self.buttons()

    def inputs(self):
        self.input_nickname = in_box.InputBox(500, 200, 140, 32)
        self.input_password = in_box.InputBox(500, 300, 140, 32)
        self.input_boxes = [self.input_nickname, self.input_password]
        self.done = False

    def labels(self):
        sign = l.Label(500, 125, "Pictures/sign_in.png")
        self.t0, self.t_rect0 = sign.getData()

        nickname = l.Label(400, 215, "Pictures/nickname.png")
        self.t1, self.t_rect1 = nickname.getData()

        password = l.Label(400, 315, "Pictures/password.png")
        self.t2, self.t_rect2 = password.getData()

    def buttons(self):
        self.x_button_ok, self.y_button_ok = 600, 400
        self.varial = False
        self.btn = b.Button('Pictures\ok.png', (self.x_button_ok, self.y_button_ok))

    def blit_labels(self):
        self.screen.blit(self.t1, self.t_rect1)
        self.screen.blit(self.t2, self.t_rect2)



    def loop(self):
        while not self.done:
            self.blit_labels()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.y_button_ok <= mouse[1] <= self.y_button_ok + 50 and self.x_button_ok - 100 <= mouse[
                        0] <= self.x_button_ok:
                                return 0

                for box in self.input_boxes:
                    box.handle_event(event)

            for box in self.input_boxes:
                box.update()

            self.screen.fill((255, 255, 255))
            for box in self.input_boxes:
                box.draw(self.screen)

            self.screen.blit(self.t0, self.t_rect0)
            self.screen.blit(self.t1, self.t_rect1)
            self.screen.blit(self.t2, self.t_rect2)

            self.btn.show(self.screen)

            pygame.display.flip()

            self.clock.tick(30)