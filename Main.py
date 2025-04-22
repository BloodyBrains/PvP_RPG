# Practice.py
""" Main file
"""

#//////////////////////////////////////////////////////////////////////////
# TO DO: 
#        Make a list of texts that need to be displayed along with their
#               positions. Append them as needed and render all during
#               draw()
#        Make game states a stack
#        Move game state constants from game_control to game_states
#        Consolidate actions.Move._get_move_tiles and make_move_buttons
#               into one.
#        Change all class 'id' attributes to 'ID' to avoid conflicts
#        Make an Agent base class for Creatures and Player to derive from
#        Use pygame sprite groups, layered updates and dirty sprites to 
#           improve performance
#        How to update cartesian positions for camera movement (CRITICAL)         
#        Change the way creatures move from using self.pos to sprite.rect (CRITICAL)
#           Or, use pygame.math.vector2 (should help with moving)
#        Variable run is not being used to break the game loop.
#        Make a camera class and possibly use culling to move only the camera, 
#           drawing only what's in the camera FOV.
#        Check how python stores instances
#        Setup RosterEdit state to show selected creature and properties
#        Change actions.Move. Agents should move themselves (IMPORTANT)
#        Call Surface.convert for all images in __init__()
#                               or
#        Move all class resource loading into class 'load' method and call
#           after pygame.init()
#           Or, make a load_image function to wrap pygame.load.image()
#
# BUGS: Rows and columns are getting swapped.
#
# RESEARCH: 
#           pygame.init() - faster to manually init pygame modules as needed?
#           pygame.sprite.Groups - put all sprites in a group for faster
#               rendering? 
#           Python dynamic inheritance for interesting way to allow users to 
#               create in-game characters

import abc
import math

import pygame
pygame.init()
pygame.font.init()
import setup


import assets
import buttons
import camera
import constants
#import client
import creatures
import creature_states
import events
import game_control
import game_states
import iso_grid
#import network
import player

#assets.load_assets()


def main():
    # SETUP /////////////////////////////////////////////////////////////////// 
    
    #!!!game = game_control.Game(ev_mgr, clock, win, cam)
    
    game = game_control.Game()
    
    

    #game.init()    

    game.run()    

    pygame.display.quit()
    pygame.quit()
    quit()





main()
