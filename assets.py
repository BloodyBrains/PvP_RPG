import os

import pygame

import constants

# TODO: Refactor asset loading to use a more dynamic approach, possibly with a config file or JSON.
# TODO: Rmove hardcoded paths and use a more flexible asset management system.
#GUI ASSET PATHS-----------------------------------------------------
menu_paths = {}
menu_paths['turn_menu_button_blank'] = os.path.join(constants.ASSETS, 'button_turn_menu_blank.png')
#button_paths = {}
#button_paths['play'] = os.path.join(constants.ASSETS, 'play_button.png')

#CREATURE ASSET PATHS------------------------------------------------
air_paths = {}
air_paths['air'] = os.path.join(constants.ASSETS, 'air.png')

battlestate_paths = {}
battlestate_paths['bgr'] = os.path.join(constants.ASSETS, 'nebula_bgr.png')
battlestate_paths['tile_selected'] = os.path.join(constants.ASSETS, 'tile_selected.png')

chaos_paths = {}
chaos_paths['chaos'] = os.path.join(constants.ASSETS, 'chaos.png')

#GRID TILE ASSET PATHS--------------------------------------------
grid_tile_paths = {}
grid_tile_paths['dirtsand'] = os.path.join(constants.ASSETS, 'tile_sanddirt.png')

#PLAYER ASSET PATHS--------------------------------------------------
player_paths = {}
player_paths['player'] = os.path.join(constants.ASSETS, 'player_wizard.png')

#GAME STATE ASSET PATHS--------------------------------------------
rosteredit_paths = {}
rosteredit_paths['bgr'] = os.path.join(constants.ASSETS, 'nebula_bgr.png')
rosteredit_paths['play'] = os.path.join(constants.ASSETS, 'play_button.png')

startstate_paths = {}
startstate_paths['bgr'] = os.path.join(constants.ASSETS, 'start_screen_bgr.png')
startstate_paths['play'] = os.path.join(constants.ASSETS, 'play_button.png')


# Load all sprites at once explicitly for now
air_sprites = {}
battlestate_sprites = {}
button_sprites = {}
chaos_sprites = {}
grid_tile_sprites = {}
player_sprites = {}
rosteredit_sprites = {}
startstate_sprites = {}
menu_sprites = {}


def load_assets():
    """Pre-loads game assets
    """
    
    for name, path in air_paths.items():
        air_sprites[name] = pygame.image.load(path).convert()
        air_sprites[name].set_colorkey((0, 0, 0))

    for name, path in battlestate_paths.items():
        battlestate_sprites[name] = pygame.image.load(path).convert()
        battlestate_sprites[name].set_colorkey((0, 0, 0))
    
    '''
    for name, path in button_paths.items():
        button_sprites[name] = pygame.image.load(path).convert()
        button_sprites[name].set_colorkey((0, 0, 0))
    '''

    for name, path in chaos_paths.items():
        chaos_sprites[name] = pygame.image.load(path).convert()
        chaos_sprites[name].set_colorkey((0, 0, 0))

    for name, path in grid_tile_paths.items():
        grid_tile_sprites[name] = pygame.image.load(path).convert()
        grid_tile_sprites[name].set_colorkey((0, 0, 0))    

    for name, path in player_paths.items():
        player_sprites[name] = pygame.image.load(path).convert()
        player_sprites[name].set_colorkey((0, 0, 0))

    for name, path in rosteredit_paths.items():
        rosteredit_sprites[name] = pygame.image.load(path).convert()
        rosteredit_sprites[name].set_colorkey((0, 0, 0))

    for name, path in startstate_paths.items():
        startstate_sprites[name] = pygame.image.load(path).convert()
        startstate_sprites[name].set_colorkey((0, 0, 0))

    #GUI assets
    for name, path in menu_paths.items():
        menu_sprites[name] = pygame.image.load(path).convert()
        menu_sprites[name].set_colorkey((0, 0, 0))

load_assets()


