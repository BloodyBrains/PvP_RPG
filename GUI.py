#HUD manager 

import abc
import os

import assets
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
        self.gui_blitlist = {} # Dict of active GUI objects to render
                              # {render_layer: ((source, dest), ...)}
        self.gui_objects = {} # Dict of registered GUI objects {menu_id: GUIobject}
        self.listen_types = [pygame.MOUSEBUTTONDOWN]
        self.render_layer = 2 # Default render layer for GUI objects


        # Switch-case dictionary of functions used to dynamically activate menus
        self._switch = {
            constants.TURN_MENU_ID: self._activate_turn_menu
        }

        register_listener(self, self.listen_types)

    def register(self, gui_obj):
        """Register a GUI object with the manager so it can be rendered.
        Sorts GUI objects by their render layer. Objects with lower render layers
        are drawn first."""

        if gui_obj.ID not in self.gui_objects:
            self.gui_objects[gui_obj.ID] = gui_obj

            if gui_obj.render_layer not in self.gui_blitlist.keys():
                self.gui_blitlist[gui_obj.render_layer] = []
                self.gui_blitlist[gui_obj.render_layer].append((gui_obj.sprite, gui_obj.pos))
                self.gui_blitlist = dict(sorted(self.gui_blitlist.items(), key=lambda item: int(item[0])))
            else:
                self.gui_blitlist[gui_obj.render_layer].append((gui_obj.sprite, gui_obj.pos))
        else:
            print(f"GUI object with ID {gui_obj.ID} is already registered.")

        


    def unregister(self, gui_obj):
        """Unregister a GUI object from the manager."""
        if gui_obj.render_layer in self.gui_blitlist:
            if gui_obj in self.gui_blitlist[gui_obj.render_layer]:
                self.gui_blitlist[gui_obj.render_layer].remove(gui_obj)
        else:
            print(f"GUI object with render layer {gui_obj.render_layer} not found in GUIManager.")


    def draw(self, game_win):
        """Draw all active GUI objects according to render_layer."""
        for render_layer, gui_objects in self.gui_blitlist.items():
            game_win.blits(self.gui_blitlist[render_layer])

    def activate_menu(self, menu_id, **kwargs):
        """Activate a specific menu by its ID and pass any additional arguments."""
        if menu_id in self._switch:
            if menu_id in self.gui_blitlist:
                print(f"Menu {menu_id} is already active")
            else:
                self._switch[menu_id](**kwargs)
        else:
            print(f"Menu with ID {menu_id} not found in GUIManager.")
        

    def deactivate_menu(self, menu_id):
        """Deactivate a specific menu by its ID."""
        if menu_id in self.gui_objects:
            obj = self.gui_objects[menu_id]
            render_layer = obj.render_layer
            sprite_pos = (obj.sprite, obj.pos)
            if render_layer in self.gui_blitlist and sprite_pos in self.gui_blitlist[render_layer]:
                self.gui_blitlist[render_layer].remove(sprite_pos)
                del self.gui_objects[menu_id]  # Remove the GUI object from the manager
        else:
            print(f"Menu with ID {menu_id} not found in GUIManager.")

    def add_button(self, button_id, pos, sprite, text=None, render_layer=3):
        """Add a button to the GUIManager."""
        button = Button(button_id, pos, sprite, text=text, render_layer=render_layer)
        self.register(button)

    # Menu activation functions
    def _activate_turn_menu(self, agent_actions):
        tmenu = TurnMenu(self, agent_actions)
        self.register(tmenu)

    def notify(self, event, **event_data):
        """Callback function from EventManager.post() to notify GUIManager
        of potential click on a GUI object.
        
        Arguments:
            event {int} -- event type (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
            event_data {dict} -- event data (mouse_pos)
        """
        handled = False
        if event == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event_data.get('event_data')
            for gui_obj in self.gui_objects.values():
                if gui_obj.rect.collidepoint(mouse_pos):
                    handled = gui_obj.notify(event, **event_data)
                    if handled:
                        break
        return handled

gui_manager = GUIManager() #Singleton
#----------------------------------------------------------------end GUIManager

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

        if self.sprite is not None:
            self.rect = pygame.Rect(self.pos, (self.sprite.get_width(), self.sprite.get_height()))

    def activate(self):
        """Activate the GUI object, making it visible and interactive.
        Register with the GUIManager and set is_active to True."""
        pass


class Button(GUIobject):

    def __init__(self, ID, sprite=None, width=0, height=0, pos=(0, 0), text=None, render_layer=3):
        super().__init__(gui_manager, ID, pos, pygame.Rect(pos, (width, height)), sprite, render_layer=render_layer)
        """Defines a clickable button.
            With no sprite, width and height are used to determine the rect.
            If sprite is used without width and height, the sprite's
                width and height determine the rect
        
            Arguments:
                id {str} -- name of button
                game_state {game_states.GameState()} -- game state to register as renderable with
            
            Keyword Arguments:
                sprite {pygame.Surface} -- button image (default: {None})
                width {int} -- button width (default: {0})
                height {int} -- button height (default: {0})
                pos {tuple} -- upper left of button (default: {(0, 0)})
                text {str} -- text to display on button (default: {None})
        """
        #self.ID = ID
        #game_state.register_renderable(self)
        #self.pos = pos
        #self.sprite = sprite
        self.is_pressed = False
        '''
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
        '''

        self.text = text
        #self.render_layer = render_layer

        #self.listen_events = (pygame.MOUSEBUTTONDOWN,)
        #events.register_listener(self, self.listen_events)  

    def update(self): pass
        # TO DO: refactor - This should only occur when the cam has moved
        #new_x = self.pos[0] + camera.offset_x
        #new_y = self.pos[1] + camera.offset_y
        #self.pos = (new_x, new_y)
    
    def action(self):
        """Action the button takes when clicked"""
        print('\nButton has not overridden Button.action()')
    
    def draw(self, win, cam_pos):
        x = self.pos[0] - cam_pos[0]
        y = self.pos[1] - cam_pos[1]  
        win.blit(self.sprite, (x, y))

    def notify(self, event, **event_data): #TODO: refactor to use GUI manager
        """Callback function from EventManager.post() to notify Button
            of potential click on the button.
        
            Arguments:
                event {int} -- event type (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
                event_data {dict} -- event data (mouse_pos)
        """
        handled = False
        if event == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event_data.get('event_data')):
                self.is_pressed = True
                events.queue_event(events.EV_BUTTON_CLICKED, button=self.ID)
                self.action()
                handled = True
        elif event == pygame.MOUSEBUTTONUP:
            self.is_pressed = False

        return handled
    
    def set_text(self, text):
        self.text = text
    
    def get_text(self):
        return self._text

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.ID
    
class RosterButton(Button):
    def __init__(self, ID, game_state, sprite=None, width=0, height=0, pos=(0, 0), text=None):
        super().__init__(ID, game_state, sprite, width, height, pos, text)
        self.name_tag = pygame.font.Font('freesansbold.ttf', 14)
        self.text_str= self.name_tag.render(self.text, True, constants.WHITE, (0, 0, 0))
        self.text_rect = self.text_str.get_rect()
        self.text_rect.center = ((self.pos[0] + (self.rect.width / 2)),
                                 (self.pos[1] + self.rect.height))

    def action(self):
        '''
        change 'selected_creature' to self
        display 'info_tag'
        '''
        pass


class ButtonTile(Button):
    """Extends the Button class to include a polygon that represents the
       isometric tile
    """
    
    def __init__(self, id, game_state, sprite=None, width=0, height=0, pos=(0, 0), iso_pos=(0, 0), text=None, polygon=None):
        """Creates a clickable iso grid tile
        
            Arguments:
                Button {class} -- clickable button
            
            Keyword Arguments:
                polygon {list[tuple(int, int)]} -- list of points that define the polygon (default: {None})
        """
        super().__init__(id, game_state, sprite, width, height, pos, text)
        self.iso_pos = iso_pos
        self.poly = polygon
        self.sprite = sprite

    '''
    def draw(self, win, cam_pos):
        x = self.pos[0] - cam_pos[0]
        y = self.pos[1] - cam_pos[1]
        win.blit(self.sprite, (x, y))
    '''

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



class TurnMenu(GUIobject):
    def __init__(self, gui_mgr, agent_actions, **kwargs):
        super().__init__(gui_mgr, 
                         ID=constants.TURN_MENU_ID,
                         pos=constants.TURN_MENU_POS,
                         sprite=assets.menu_sprites['turn_menu_button_blank'], #TODO: hardcode
                         **kwargs)
        #events.register_listener(self, constants.MOUSELEFT)
        self.agent_actions = agent_actions # Buttons to create for the active agent
        #button_blank = pygame.image.load(os.path.join(constants.ASSETS, 'button_turn_menu_blank.png'))
        #font = pygame.font.SysFont('Arial', 10)
        #button_width = button_blank.get_width()
        #button_height = button_blank.get_height()


        buttons = {}
        for i, action in enumerate(agent_actions):
            buttons[action] = Button(ID=action, 
                                    sprite=self.sprite, 
                                    pos=(self.pos[0], self.pos[1] + (i * self.sprite.get_height())),
                                    text=action)

        #self.is_active = False

    def activate(self, items):
        #register_listener(self, pygame.MOUSEBUTTONDOWN)
        gui_manager.register(self)

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
        


    def add_buttons(self, *button_ids):
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



    
        