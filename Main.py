# Practice.py
""" Main file
"""

#//////////////////////////////////////////////////////////////////////////


import math

import pygame
pygame.init()
pygame.font.init()
import setup


import assets
import buttons
import camera
import constants
import creatures
import creature_states
import events
import game_control
import game_states
import iso_grid
import player



def main():
    # Initialize /////////////////////////////////////////////////////////////////// 
    #     Currently, all assets are loaded at startup when assets.py is imported.
        
    game = game_control.Game()   


    game.run()    

    pygame.display.quit()
    pygame.quit()
    quit()


main()
