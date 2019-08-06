# iso_grid.py

# TO DO:
#       Bind camera movement to remain within the map

import os

import pygame

import constants


class IsoGrid():
    tiles = {}
    tiles['dirtsand'] = pygame.image.load(os.path.join(constants.ASSETS, 'tile_sanddirt.png'))
    #iso_tile.set_colorkey((0, 0, 0))

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

    rows = len(map_data)


    TILE_WIDTH = 192
    TILE_HEIGHT = 96

    velocity_x = 0
    offset_x = 0
    velocity_y = 0
    offset_y = 0

    start_x = constants.CAM_STARTX
    start_y = constants.CAM_STARTY

    tile = None

    @classmethod
    def draw_tiles(cls, game_win):
        for row_iter, row in enumerate(cls.map_data):
            for col, tile in enumerate(row):
                if tile == 0:
                    surf = cls.tiles['dirtsand']

                cart_x = (col * (cls.TILE_WIDTH / 2)) + (row_iter * (cls.TILE_WIDTH / 2))
                cart_y = -(col * (cls.TILE_HEIGHT /2)) + (row_iter * (cls.TILE_HEIGHT /2))
                game_win.blit(surf, (cls.start_x + cart_x + cls.offset_x, 
                                     cls.start_y + cart_y + cls.offset_y))

    @classmethod
    def update(cls):
        cls.offset_x += cls.velocity_x
        cls.offset_y += cls.velocity_y