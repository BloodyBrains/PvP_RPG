"""Main controller for game flow
"""

import assets
from camera import Camera
from events import EventManager
import iso_grid

tile_grid = None
ev_mgr = None


def controller_tick():
    """Handles player input
    """
    pass

def view_tick():
    """Handles the the updates
    """
    pass


def init():
    # Load assets
    assets.load_assets()

    # Init game entities
    global tile_grid, ev_mgr

    tile_grid = iso_grid.IsoGrid(assets.grid_tiles_sprites)
    ev_mgr = EventManager()


def update():
    events = ev_mgr.get_events()  
    Camera.update()
    tile_grid.update()

def draw(game_win):
    tile_grid.draw_tiles(game_win)

def quit(): pass


states = {}     # Dict of game_states.GameState referring to 'screens'
managers = {}   # Dict of managers.Manager to delegate game operations

running = True  # Sentinel for the main game loop
