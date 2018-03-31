from main import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = pygame.Color('antiquewhite4')
COLOR_ACTIVE = pygame.Color('black')
FONT = pygame.font.Font(None, 32)


class Label:
    font = pygame.font.Font(None, 50)

    def __init__(self,x,y, text):
        self.t1 = self.font.render(text, True, (0, 0, 0))
        self.t_rect1 = self.t1.get_rect()
        self.t_rect1.centerx, self.t_rect1.centery = x,y


    def getData(self):
        return self.t1, self.t_rect1

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(300, 100, 140, 32)
    input_box2 = InputBox(300, 200, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    label1 = Label(200, 115, "Nickname")
    t1, t_rect1 = label1.getData()

    label2 = Label(200, 215, "Password")
    t2, t_rect2 = label2.getData()

    x_button_exit, y_button_exit = 400,300
    varial = False

    while not done:
        screen.blit(t1, t_rect1)
        screen.blit(t2, t_rect2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if y_button_exit<= mouse[1] <= y_button_exit+50 and x_button_exit-100<=mouse[0]<=x_button_exit:
                    # dodanie akcji do przycisku - logowanie z bd, przejscie do ekranu kolejnego :)
                    varial = True

            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((255, 255, 255))
        for box in input_boxes:
            box.draw(screen)

        screen.blit(t1, t_rect1)
        screen.blit(t2, t_rect2)

        login = Buttonify('exit.png', (400, 300), screen)

        pygame.display.flip()

        clock.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()