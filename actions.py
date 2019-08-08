# actions.py
"""Actions an agent can perform

Returns:
    [type] -- [description]
"""
import abc
import os

import pygame

import buttons
import camera
import constants
from functions import iso_to_cart


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
    def run(self): pass

    @abc.abstractmethod
    def end(self): pass

    @abc.abstractmethod
    def draw(self, game_win): pass

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

    def __init__(self, owner):
        super().__init__(owner)
        self.valid_moves = None     #List of tiles the agent can move to (cartesian)
        self.selected_tile = None   #Tile the agent needs to move to
        self.has_moved = False          #Set True after agent moves
        self.tile_buttons = None    #List of buttons for all tiles in valid_moves
        self.is_drawing = False
        self.first_pos = (0, 0)     #Move along the isometric x row
        self.distance1 = 0
        self.distance2 = 0
        self.second_pos = (0, 0)    #Move along the isometric y column
        self.slope = 0

    def check_reqs(self):
        return not self.has_moved

    def start(self):
        self._get_move_tiles()
        self.is_drawing = True

    def run(self):
        """
            set agents velocity vector towards the clicked tiles x column 
            move there
            set agents velocity vector toward the clicked tiles y column 
            move there
            call self.end()
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
                if self.distance2 <= 0: #we moved to the first position
                    self.selected_tile = None
                    distance2 = 0

    def end(self): pass       

    def draw(self, game_win):
        if self.is_drawing:
            for tile in self.valid_moves:
                game_win.blit(self.tile_img, (tile[0], tile[1]))

    def check_click(self, mouse_pos):
        for button in self.tile_buttons:
            if button.check_click(mouse_pos):
                self.selected_tile = button.iso_pos
                self.first_pos = (button.iso_pos[0], self._owner.iso_pos[1])
                self.distance1 = abs(self._owner.iso_pos[0] - self.first_pos[0]) * constants.TILE_W_HALF
                self.distance2 = abs(self.first_pos[1] - self.selected_tile[1]) * constants.TILE_W_HALF
                print(button.iso_pos)  
                self.reset()
                return True
                break
        return False

    def reset(self):
        self.valid_moves = None     
        #self.selected_tile = None   
        self.has_moved = False          
        self.tile_buttons = None
        self.is_drawing = False


    def _get_move_tiles(self):
        """Makes a list of tiles the agent can move to and sets it
           to the owners valid_moves list
        """
        # TO DO: check if tiles can be moved to
        self.valid_moves = []
        iso_tiles = []
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
                iso_tiles.append((self._owner.iso_pos[0] + x, self._owner.iso_pos[1] + y))
                y += 1
            x += 1
            y = -(self._owner.move_amount - abs(x))

        for tile in iso_tiles:
            self.valid_moves.append(iso_to_cart(tile, with_offset=1))

        self.make_move_buttons(iso_tiles) #Use the iso_tiles to make button ids

    def make_move_buttons(self, tiles):
        """Makes a list of buttons.Button objects from 'tiles' that can be
            clicked on
            
            Arguments:
                tiles {list(int, int)} -- self.valid_moves
        """
        self.tile_buttons = []
        i = 0
        for tile in self.valid_moves:
            p1 = (tile[0], tile[1] + constants.TILE_H_HALF)
            p2 = (tile[0] + constants.TILE_W_HALF, tile[1])
            p3 = (tile[0] + constants.TILE_WIDTH, tile[1] + constants.TILE_W_HALF)
            p4 = (tile[0] + constants.TILE_W_HALF, tile[1] + constants.TILE_HEIGHT)
            poly = [p1, p2, p3, p4]

            self.tile_buttons.append(buttons.ButtonTile(str(tiles[i]),
                                                    width=constants.TILE_WIDTH,
                                                    height=constants.TILE_HEIGHT,
                                                    pos=(tile[0], tile[1]),
                                                    iso_pos=tiles[i],
                                                    polygon=poly))
            i += 1

