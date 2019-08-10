#GLOBALS
import os

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_WIDTH = 192
TILE_HEIGHT = 96
TILE_W_HALF = 96
TILE_H_HALF = 48
CREATURE_W = 96     # dimensions of creature sprite
CREATURE_H = 80
CAM_SPEED = 3
CAM_STARTX = -672
CAM_STARTY = 96
MOVE_SPEED = 3
SLOPE_MOVE = (2, 1) # kinda like a slope for moving along an 
                    #   isometric row/column
