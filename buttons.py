# buttons.py
import pygame

import camera
import constants


class Button():
    def __init__(self, ID, sprite=None, width=0, height=0, pos=(0, 0), text=None):
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
        self.ID = ID
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

    def draw(self, win):
        win.blit(self.sprite, self.pos)

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self._text

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.ID


class ButtonTile(Button):
    """Extends the Button class to include a polygon that represents the
       isometric tile
    """
    
    def __init__(self, id, sprite=None, width=0, height=0, pos=(0, 0), iso_pos=(0, 0), text=None, polygon=None):
        """Creates a clickable iso grid tile
        
            Arguments:
                Button {class} -- clickable button
            
            Keyword Arguments:
                polygon {list[tuple(int, int)]} -- list of points that define the polygon (default: {None})
        """
        super().__init__(id, sprite, width, height, pos, text)
        self.iso_pos = iso_pos
        self.poly = polygon
        self.sprite = sprite

    def check_click(self, mouse_pos):
        """Returns if the polygon contains the mouse_pos or not
        
            Arguments:
                mouse_pos {tuple(int, int)} -- mouse position
            
            Returns:
                bool -- True if polygon contains mouse_pos
        """
        n = len(self.poly)
        x = mouse_pos[0]
        y = mouse_pos[1]
        inside =False

        p1x,p1y = self.poly[0]
        for i in range(n+1):
            p2x,p2y = self.poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside