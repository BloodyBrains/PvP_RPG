#HUD manager 

import abc
import os

import pygame
import buttons
import constants
from events import register_listener




class HudObject(abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        '''
        pos[x,y]
        rect
        sprite
        font
        font_size
        clickable
        
        '''


class TurnMenu(HudObject):
    def __init__(self, ) -> None:
        super().__init__()
        #events.register_listener(self, constants.MOUSELEFT)
        button_blank = pygame.image.load(os.path.join(constants.ASSETS, 'button_turn_menu_blank.png'))
        font = pygame.font.SysFont('Arial', 10)
        button_width = button_blank.get_width()
        button_height = button_blank.get_height()
        pos = (100, 370)
        buttons = {}
        is_active = False

    def activate(self, items):
        register_listener(self, pygame.MOUSEBUTTONDOWN)
        self.buttons = {}
        i = 0
        for item in items:
            self.buttons[item] = Button(item, 
                                       self.button_blank, 
                                       pos=(self.pos[0], self.pos[1] + (i * self.button_height)),
                                       text=item)
            i += 1

        self.is_active = True

    def deactivate(self):
        self.ev_mgr.unregister_listener(self)
        self.is_active = False


    @classmethod
    def update(cls):
        '''
        new_x = cls.pos[0] + camera.offset_x
        new_y = cls.pos[1] + camera.offset_y
        cls.pos = (new_x, new_y)

        for button in cls.buttons.values():
            button.update()
        '''
        pass

    def draw(self, game_win):
        for button in self.buttons.values():
            text = self.font.render(button.ID, False, (0, 0, 0))
            game_win.blit(self.button_blank, button.pos)
            game_win.blit(text, (button.pos[0] + 10, button.pos[1]  + 5))


    def notify(self, event): pass
        


    @classmethod
    def add_buttons(cls, *button_ids):
        for button in button_ids:
            cls.buttons[button] = Button(button,
                                          cls.button_blank,
                                          (0, 0),
                                          button)
            print(cls.buttons)

    def populate(self, valid_actions):
        """Populates the turn_menu with buttons from the valid_actions 
               passed in from the active_player
        
        Arguments:
            valid_actions {list(str)} -- [list of players valid actions]
        """
        pass

class HUDManager:
    # Responsible for HUD related logic and objects.
    # eg. update, draw, instantiation, event delegation
    #       for menus, maps etc.

    active_HUDs = list(None)

    def __init__(self) -> None:
        pass

    def update(self): pass

    def draw(self): pass

    
        