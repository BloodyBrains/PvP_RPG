#GLOBALS
import os

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')

#RGB for pygame text
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

#FONTS:
DEFAULT_FONT = 'freesansbold.ttf'
DEFAULT_FONT_SIZE = 14

#Graphics
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_WIDTH = 192
TILE_HEIGHT = 96
TILE_W_HALF = 96
TILE_H_HALF = 48
CREATURE_W = 96     # dimensions of creature sprite
CREATURE_H = 80
CAM_SPEED = 3
CAM_STARTX = 0 #-672
CAM_STARTY = 0 #96
MOVE_SPEED = 3
SLOPE_MOVE = (2, 1) # kinda like a slope for moving along an 
                    #   isometric row/column


# GUI Constants----------------------
    # Menu IDs
TURN_MENU_ID = 'turn_menu'

#    Menu positions
TURN_MENU_POS = (100, 370)


# Event types
EV_NONE = -1
EV_ALL = 0
EV_QUIT = 1
EV_KEY_LEFT = 2
EV_KEY_RIGHT = 3
EV_KEY_UP = 4
EV_KEY_DOWN = 5
EV_KEY_LEFT_UP = 6
EV_KEY_RIGHT_UP = 7
EV_KEY_UP_UP = 8
EV_KEY_DOWN_UP = 9
EV_MOUSE_CLICK = 10
EV_UPDATE = 11
EV_AGENT_CLICKED = 12
EV_CAM_MOVE = 13
EV_ACTION_END = 14
EV_TILE_CLICKED = 15
