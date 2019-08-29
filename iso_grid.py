# iso_grid.py

# TO DO:
#       Bind camera movement to remain within the map

import os

import pygame

import assets
import camera
import constants


class IsoGrid():
    TILE_WIDTH = 192
    TILE_HEIGHT = 96

    def __init__(self, event_manager):
        self.ev_mgr = event_manager
        self.listen_types = []
        event_manager.register_listener(self, self.listen_types)
        self.pos = (0, 0)
        self.x_speed = 0
        self.y_speed = 0
        self.tiles = assets.grid_tile_sprites
        #self.tiles['dirtsand'] = pygame.image.load(os.path.join(constants.ASSETS, 'tile_sanddirt.png'))
        #iso_tile.set_colorkey((0, 0, 0))

        self.map_data = [
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

        rows = len(self.map_data)


        

        velocity_x = 0
        offset_x = 0
        velocity_y = 0
        offset_y = 0

        self.start_x = constants.CAM_STARTX
        self.start_y = constants.CAM_STARTY

        tile = None


    def draw_tiles(self, game_win):
        for row_iter, row in enumerate(self.map_data):
            for col, tile in enumerate(row):
                if tile == 0:
                    surf = self.tiles['dirtsand']

                cart_x = (col * (self.TILE_WIDTH / 2)) + (row_iter * (self.TILE_WIDTH / 2))
                cart_y = -(col * (self.TILE_HEIGHT /2)) + (row_iter * (self.TILE_HEIGHT /2))
                game_win.blit(surf, (self.pos[0] + cart_x, 
                                     self.pos[1] + cart_y))

    def update(self):
        x = self.pos[0] + self.x_speed
        y = self.pos[1] + self.y_speed
        self.pos = (x, y)
