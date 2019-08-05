# buttons.py

import pygame

import camera


class Button():
    def __init__(self, id, sprite, pos=(0, 0), text=None):
        self.id = id
        self.pos = pos
        self.sprite = sprite
        self.is_pressed = False
        self.rect = pygame.Rect((self.pos), 
                               (self.sprite.get_width(), self.sprite.get_height()))
        self.text = text

    def update(self):
        # TO DO: refactor - This should only occur when the cam has moved
        new_x = self.pos[0] + camera.offset_x
        new_y = self.pos[1] + camera.offset_y
        self.pos = (new_x, new_y)

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self._text

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.id
