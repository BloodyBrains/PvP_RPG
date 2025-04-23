#HUD manager 

import abc
import os

import pygame
import buttons
import constants
from events import register_listener


class GUIManager:
    """
    Manages GUI objects in the game.
    Handles activation, deactivation, and rendering of GUI objects.
    """
    
    def __init__(self):
        self.gui_objects = {}
        self.active_gui = None

    def register_gui(self, gui_object):
        """Register a GUI object with the manager."""
        self.gui_objects[gui_object.ID] = gui_object

    def activate_gui(self, gui_id):
        """Activate a GUI object by its ID."""
        if gui_id in self.gui_objects:
            if self.active_gui:
                self.active_gui.deactivate()
            self.active_gui = self.gui_objects[gui_id]
            self.active_gui.activate()

    def draw(self, game_win):
        """Draw all active GUI objects."""
        if self.active_gui and self.active_gui.is_active:
            self.active_gui.draw(game_win)

class GUIobject(abc.ABC):
    """
    Abstract base class for GUI objects in the game.
    """
    
    def __init__(self, gui_mgr, ID="menu", pos=(0, 0), rect=pygame.Rect(0,0,32,32), sprite=None, 
                 font=(None, constants.DEFAULT_FONT_SIZE),
                 render_layer=2) -> None:
        super().__init__()
        self.gui_mgr = gui_mgr
        self.ID = ID
        self.pos = pos
        self.rect = rect
        self.sprite = sprite
        self.font = pygame.font.Font(font[0], font[1])
        self.render_layer = render_layer

        self.is_active = False

    @abc.abstractmethod
    def activate(self):
        """Activate the GUI object, making it visible and interactive.
        Register with the GUIManager and set is_active to True."""
        pass



class TurnMenu(GUIobject):
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



    
        