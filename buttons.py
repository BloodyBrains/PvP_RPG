# buttons.py

import pygame

import camera


class Button():
    def __init__(self, id, sprite=None, width=0, height=0, pos=(0, 0), text=None):
        """Defines a clickable button.
            With no sprite, width and height are used to determine the rect.
            If sprite is used without width and height, the sprite's
                width and height determine the rect
        
        Arguments:
            id {str} -- name of button
        
        Keyword Arguments:
            sprite {pygame.Surface} -- button image (default: {None})
            width {int} -- button width (default: {0})
            height {int} -- button height (default: {0})
            pos {tuple} -- upper left of button (default: {(0, 0)})
            text {str} -- text to display on button (default: {None})
        """
        self.id = id
        self.pos = pos
        self.sprite = sprite
        self.is_pressed = False
        if sprite == None:
            self.rect = pygame.Rect((self.pos),
                                    (width, height))
        else:
            if (width == 0) and (height == 0):
                self.rect = pygame.Rect((self.pos), 
                                        (self.sprite.get_width(), self.sprite.get_height()))
            else:
                self.rect = pygame.Rect((self.pos), 
                                        (width, height))

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
