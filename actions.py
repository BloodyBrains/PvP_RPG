# actions.py
"""Actions an agent can perform

"""
import abc
import os

import pygame

import buttons
import camera
import constants
from functions import iso_to_cart


HOOKS = {}

class Action:
    def __init__(self, owner):
        self._owner = owner
        self.is_drawing = False

    @abc.abstractmethod
    def check_reqs(self):
        """Use to check if the owner has the requirements to perform
                the action. If so, add the action ID to the agents
                valid_actions list
            Returns bool
        """
        pass

    @abc.abstractmethod
    def start(self):
        """Performs setup work for the action
        """
        pass

    @abc.abstractmethod
    def update(self): pass

    @abc.abstractmethod
    def run(self): pass

    @abc.abstractmethod
    def end(self): pass

    @abc.abstractmethod
    def handle_input(self, event, *args): 
        """Called from game_states.BattleState.update to handle user
            input events that are specific to the Action.
            
            Arguments:
                event {pygame.event} -- pygame event
        """
        pass

    @abc.abstractmethod
    def draw(self, game_win, cam_pos): pass

    @abc.abstractmethod
    def check_click(self, mouse_pos): pass

    @abc.abstractmethod
    def reset(self):
        """Sets the Action instance attributes to initial state
        """
        pass


class Move(Action):
    tile_img = pygame.image.load(os.path.join(constants.ASSETS, 'move_tile.png'))
    #tile.set_alpha(100)
    ID = 'move'

    @staticmethod
    def check_reqs(owner):
        print(str(owner.has_moved))
        return not owner.has_moved

    hook = {ID: check_reqs}

    def __init__(self, owner):
        super().__init__(owner)
        self.events_to_handle = [
            constants.EV_MOUSE_CLICK
        ]
        self.valid_moves = None     #List of tiles the agent can move to (cartesian)
        self.iso_tiles = None       #List of iso tiles the player can move to
        self.selected_tile = None   #Tile the agent needs to move to
        self.has_moved = False      #Set True after agent moves
        self.tile_buttons = []      #List of buttons for all tiles in valid_moves
        self.first_pos = (0, 0)     #Move along the isometric x row
        self.distance1 = 0
        self.distance2 = 0
        self.second_pos = (0, 0)    #Move along the isometric y column
        self.slope = 0


    def start(self):
        self._get_move_tiles()

    def update(self): pass

    def run(self):
        """ Moves the agent to the selected tile in two moves (if neccessary)
            First, moves the column position, then to the row position.
            Call self.end()
        """

        direction = 1 
        if self.selected_tile is not None:
            if self.first_pos is not None:
                # calculate which direction to use
                if self._owner.iso_pos[0] > self.first_pos[0]:
                    direction = -direction # use negative slope
                new_pos = (self._owner.pos[0] + ((constants.SLOPE_MOVE[0] * constants.MOVE_SPEED) * direction),
                           self._owner.pos[1] - ((constants.SLOPE_MOVE[1] * constants.MOVE_SPEED) * direction))
                self.distance1 -= abs(self._owner.pos[0] - new_pos[0])
                self._owner.pos = new_pos
                if self.distance1 <= 0: #we moved to the first position
                    self._owner.iso_pos = self.first_pos
                    self.first_pos = None
                    distance1 = 0
            else: 
                if self._owner.iso_pos[1] > self.selected_tile[1]:
                    direction = -direction
                new_pos = (self._owner.pos[0] + ((constants.SLOPE_MOVE[0] * constants.MOVE_SPEED) * direction),
                           self._owner.pos[1] + ((constants.SLOPE_MOVE[1] * constants.MOVE_SPEED) * direction))
                self.distance2 -= abs(self._owner.pos[0] - new_pos[0])
                self._owner.pos = new_pos
                if self.distance2 <= 0: #we moved to the final position
                    self._owner.iso_pos = self.selected_tile
                    self._owner.pos = iso_to_cart(self._owner.iso_pos, self._owner.width, self._owner.height, with_offset=1)
                    self.selected_tile = None
                    self.end()
                    distance2 = 0

    def end(self):
        self.has_moved = True

    def handle_input(self, event, *args):
        handled = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = args[0]
            for butt in self.tile_buttons:
                if butt.rect.collidepoint(mouse_pos):
                    print("clicked on move tile!")
                    handled = True
        
        return handled

    def draw(self, game_win, cam_pos):
        for but in self.tile_buttons:
            but.draw(game_win, cam_pos)

    def check_click(self, mouse_pos):
        """ Checks if a tile has been clicked on to move to.
            If so, it calculates the iso pos of the first move and the
            x distance to get there.
            Calls reset()
            Arguments:
                mouse_pos {tuple(int)} -- mouse position
            
            Returns:
                bool -- True if a valid tile is clicked
        """

        for button in self.tile_buttons:
            if button.check_click(mouse_pos):
                self.selected_tile = button.iso_pos
                self.first_pos = (button.iso_pos[0], self._owner.iso_pos[1])
                self.distance1 = abs(self._owner.iso_pos[0] - self.first_pos[0]) * constants.TILE_W_HALF
                self.distance2 = abs(self.first_pos[1] - self.selected_tile[1]) * constants.TILE_W_HALF
                print(button.iso_pos)  
                self.reset()
                return True
        return False
        #TO DO: Break this into separate methods

    def reset(self):
        self.valid_moves = []    
        self.tile_buttons = []


    def _get_move_tiles(self):
        """Makes a list of tiles the agent can move to and sets it
           to the owners valid_moves list
        """
        # TO DO: check if tiles can be moved to
        self.valid_moves = []
        self.iso_tiles = []
        '''
         Assemble list of all valid tiles the agent can move to.
         Outer loop starts with the most negative valid x pos.
         Inner loop starts with the most negative valid y pos for given x
         e.g. With a move_amount of 2 from pos(0, 0), the append 
                   order will be:
                   (-2, 0)
                   (-1, -1), (-1, 0), (-1, 1)
                   (0, -2), (0, -1), (0, 0), (0, 1), (0, 2)
                   (1, -1), (1, 0), (1, 1) 
                   (2, 0)
        '''
        x = -(self._owner.move_amount)
        y = -(self._owner.move_amount - abs(x))
        while x <= self._owner.move_amount:
            while y <= (self._owner.move_amount - abs(x)):
                self.iso_tiles.append((self._owner.iso_pos[0] + x, self._owner.iso_pos[1] + y))
                y += 1
            x += 1
            y = -(self._owner.move_amount - abs(x))

        for tile in self.iso_tiles:
            self.valid_moves.append(iso_to_cart(tile))

        #self.make_move_buttons(iso_tiles) #Use the iso_tiles to make button ids

    def make_move_buttons(self):
        """Makes a list of buttons.Button objects from 'tiles' that can be
            clicked on
            
            Arguments:
                tiles {list(int, int)} -- self.valid_moves
        """
        self.tile_buttons = []
        i = 0
        for tile in self.valid_moves:
            # Assemble the polygon that represents the clickable area of the tile
            p1 = (tile[0], tile[1] + constants.TILE_H_HALF)
            p2 = (tile[0] + constants.TILE_W_HALF, tile[1])
            p3 = (tile[0] + constants.TILE_WIDTH, tile[1] + constants.TILE_W_HALF)
            p4 = (tile[0] + constants.TILE_W_HALF, tile[1] + constants.TILE_HEIGHT)
            poly = [p1, p2, p3, p4]

            self.tile_buttons.append(buttons.ButtonTile(str(self.iso_tiles[i]),
                                                    sprite=self.tile_img,
                                                    pos=tile,
                                                    iso_pos=self.iso_tiles[i],
                                                    polygon=poly))
            i += 1


    def adjust_positions(self, cam_pos):
        i = 0
        for tile in self.valid_moves:
            x = tile[0] - cam_pos[0]
            y = tile[1] - cam_pos[1]
            self.valid_moves[i] = (x, y)
            i += 1

HOOKS["move"] = Move.check_reqs


#---------------------------------------------------------------------------------------
def get_action(action_id, owner):
    if action_id == 'move':
        return Move(owner)
    else:
        print("error: no actions.Action: ", action_id)

