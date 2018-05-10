import hashlib
import pygame
from pymongo import MongoClient
import os

class InputBox:

    pygame.init()
    COLOR_INACTIVE = pygame.Color('antiquewhite4')
    COLOR_ACTIVE = pygame.Color('black')
    FONT = pygame.font.Font(None, 32)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
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
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
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
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


    def checkWithMongo(self, nick, password):
        client = MongoClient('localhost', 27017)
        db = client['BomberMan']
        collection = db['Players']

        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        print(sha_signature)

        answer = (collection.find({"login": nick, "password": sha_signature}).count()) == 1

        if(answer): return 1
        else: return 0