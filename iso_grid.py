# iso_grid.py

# TO DO:
#       Bind camera movement to remain within the map.
#       Notify() should be a forced implementation.

import os

import pygame

import assets
import camera
import constants
import events
from globals import GlobalState


class IsoGrid():
    TILE_WIDTH = 192
    TILE_HEIGHT = 96

    listen_types = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, )
    tiles = assets.grid_tile_sprites
    render_layer = 0

    def __init__(self):
        #self.ev_mgr = event_manager
        #self.listen_types = []
        events.register_listener(self, self.listen_types)
        self.pos = (0, 0)
        self.x_speed = 0
        self.y_speed = 0
        #self.tiles = assets.grid_tile_sprites
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


    def draw_tiles(self, game_win, cam_pos):
        '''
        for row_iter, row in enumerate(self.map_data):
            for col, tile in enumerate(row):
                if tile == 0:
                    surf = self.tiles['dirtsand']

                cart_x = (col * (self.TILE_WIDTH / 2)) + (row_iter * (self.TILE_WIDTH / 2))
                cart_y = -(col * (self.TILE_HEIGHT /2)) + (row_iter * (self.TILE_HEIGHT /2))
                game_win.blit(surf, (self.pos[0] + (cart_x - cam_pos[0]), 
                                     self.pos[1] + (cart_y - cam_pos[1])))
        '''
        render_list = []
        for row_iter, row in enumerate(self.map_data):
            for col, tile in enumerate(row):
                if tile == 0:
                    surf = self.tiles['dirtsand']

                cart_x = (col * (self.TILE_WIDTH / 2)) + (row_iter * (self.TILE_WIDTH / 2))
                cart_y = -(col * (self.TILE_HEIGHT /2)) + (row_iter * (self.TILE_HEIGHT /2))
                render_list.append((surf, (self.pos[0] + (cart_x - cam_pos[0]), 
                                           self.pos[1] + (cart_y - cam_pos[1]))))
                
        game_win.blits(render_list)
                

    def update(self):
        x = self.pos[0] + self.x_speed
        y = self.pos[1] + self.y_speed
        self.pos = (x, y)
        if self.x_speed:
            print("x_speed: ", self.x_speed)

    def notify(self, event, **event_data):
        """Callback function from EventManager.post() to notify IsoGrid
            of potential click on a grid tile.
        
            Arguments:
                event {int} -- event type (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
                event_data {dict} -- event data (mouse_pos)
        """
        
        if event == pygame.MOUSEBUTTONDOWN:
            print("mouse down")
            clicked_tile = self.check_tile_click(event_data.get('event_data')) 
            events.queue_event(events.EV_TILE_CLICKED, clicked_tile = clicked_tile)
        if event == pygame.MOUSEBUTTONUP:
            print("mouse up")

    #def check_tile_click(self, click_pos):
        """Check if the mouse click is on a tile.
        
            Arguments:
                event {int} -- event type
                event_data {dict} -- event data
        """
        '''
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] + self.pos[0]
        mouse_y = mouse_pos[1] + self.pos[1]

        col = int((mouse_x / self.TILE_WIDTH) + (mouse_y / self.TILE_HEIGHT)) % len(self.map_data[0])
        row = int((mouse_y / self.TILE_HEIGHT) - (mouse_x / self.TILE_WIDTH)) % len(self.map_data)

        print("col: ", col, "row: ", row)
        '''

    
    def check_tile_click(self, mouse_pos):
        """
        Converts the mouse position to the corresponding tile in the isometric grid.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse.

        Returns:
            tuple: The (row, col) of the clicked tile, or None if out of bounds.
        """
        # Adjust mouse position based on grid offset
        mouse_x, mouse_y = mouse_pos
        cam_pos = GlobalState.active_camera.pos
        mouse_x += cam_pos[0]
        mouse_y += cam_pos[1]

        # Convert screen coordinates to isometric grid coordinates
        row = int((mouse_x / constants.TILE_WIDTH - mouse_y / constants.TILE_HEIGHT))
        col = int((mouse_y / constants.TILE_HEIGHT + mouse_x / constants.TILE_WIDTH))
        # Check if the calculated tile is within bounds
        if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[0]):
            print(f"Tile clicked at row {row}, col {col}")
            print(f"pos: {self.pos})")
            print(f"cam_pos: {cam_pos}")
            return row, col
        return None


# END OF FILE /////////////////////////////////////////////////////////////////