"""Isometric tile grid used for the battlefield.
    iso_pos refers to the (row, column) pos of the tile relative to the grid
    pos refers to the tile's sprite pos relative to the game_win
"""

# TO DO:
#       Bind camera movement to remain within the map

import os

import pygame

from camera import Camera
import constants


# Tile constants
DIRTSAND = 0


class IsoGrid():
    pos = (0, 0)
    tiles = {}
    map_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]


    @classmethod
    def __init__(cls, tile_sprites):
        cls.tiles = tile_sprites


    @classmethod
    def draw_tiles(cls, game_win):
        for row_iter, row in enumerate(cls.map_data):
            for col, tile in enumerate(row):
                if tile == DIRTSAND:
                    surf = cls.tiles['dirtsand']

                cart_x = (col * (constants.TILE_W_HALF)) + (row_iter * (constants.TILE_W_HALF))
                cart_y = -(col * (constants.TILE_H_HALF)) + (row_iter * (constants.TILE_H_HALF))
                game_win.blit(surf, (cls.pos[0] + cart_x, 
                                     cls.pos[1] + cart_y))

    @classmethod
    def update(cls):
        # Update position relative to the camera
        cls.pos = (cls.pos[0] - Camera.pos[0], cls.pos[1] - Camera.pos[1])
