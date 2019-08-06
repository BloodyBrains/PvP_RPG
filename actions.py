# actions.py
"""Actions an agent can perform

Returns:
    [type] -- [description]
"""
import abc
import os

import pygame

import camera
import constants
from functions import iso_to_cart


class Action:
    def __init__(self, owner):
        self._owner = owner

    @abc.abstractmethod
    def check_reqs(self):
        """Use to check if the owner has the requirements to perform
                the action. If so, add the action ID to the agents
                valid_actions list
            Returns bool
        """
        pass

    @abc.abstractmethod
    def run(self): pass

    @abc.abstractmethod
    def draw(self, game_win): pass


class Move(Action):
    tile_img = pygame.image.load(os.path.join(constants.ASSETS, 'move_tile.png'))
    #tile.set_alpha(100)
    ID = 'move'

    def __init__(self, owner):
        super().__init__(owner)
        self.moved = False #Set True after agent moves

    def check_reqs(self):
        return not self.moved

    def run(self):
        self._get_move_tiles()


    def _get_move_tiles(self):
        """Makes a list of tiles the agent can move to and sets it
           to the owners valid_moves list
        """
        # TO DO: check if tiles can be moved to
        tiles = []
        
        # Assemble list of all valid tiles the agent can move to.
        # Outer loop starts with the most negative valid x pos.
        # Inner loop starts with the most negative valid y pos for given x
        # e.g. With a move_amount of 2 from pos(0, 0), the append 
        #           order will be:
        #           (-2, 0)
        #           (-1, -1), (-1, 0), (-1, 1)
        #           (0, -2), (0, -1), (0, 0), (0, 1), (0, 2)
        #           (1, -1), (1, 0), (1, 1) 
        #           (2, 0)
        x = -(self._owner.move_amount)
        y = -(self._owner.move_amount - abs(x))
        while x <= self._owner.move_amount:
            while y <= (self._owner.move_amount - abs(x)):
                tiles.append((self._owner.iso_pos[0] + x, self._owner.iso_pos[1] + y))
                y += 1
            x += 1
            y = -(self._owner.move_amount - abs(x))

        tiles_cart = []
        for tile in tiles:
            tiles_cart.append(iso_to_cart(tile))

        self._owner.valid_moves = tiles_cart

        # draw move_tile on all valid tiles
        # check for click on valid tiles
        # set agents velocity vector towards the clicked tiles
        #       x column and move there
        # set agents velocity vector toward the clicked tiles
        #       y column and move there

    def draw(self, game_win):
        #if self.is_waiting_
        for tile in self._owner.valid_moves:
            game_win.blit(self.tile_img, (tile[0] + camera.offset_x, tile[1] + camera.offset_y))
