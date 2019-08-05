# Practice.py
""" Main file
"""

#//////////////////////////////////////////////////////////////////////////
# TO DO: 
#        Make a list of creature instances for game_states.RosterEdit.roster
#        Make a file for general purpose methods: iso_to_cart() 
#        Change all class 'id' attributes to 'ID' to avoid conflicts
#        Make an Agent base class for Creatures and Player to derive from
#        Make a camera class to store the camera offset and add it to
#           instances positions in update() (remove from draw()).
#           Or, research culling and possibly move only the camera, drawing
#           only what's in the camera FOV.
#           Or, use an Observer pattern to call pos_update(cam_offset) for 
#           all instances currently being rendered. Set a flag when a
#           camera move event is registered and only check once per update
#           if the flag has been set           
#        Change the way creatures move from using self.pos to self.rect
#        Check how python stores instances
#        Setup RosterEdit state to show selected creature and properties
#        Call Surface.convert for all images in __init__()
#                               or
#        Move all class resource loading into class 'load' method and call
#           after pygame.init()
#
# RESEARCH: 
#           pygame.init() - faster to manually init pygame modules as needed?
#           pygame.sprite.Groups - put all sprites in a group for faster
#               rendering? 

import abc
import math

import pygame
pygame.init()
pygame.font.init()

import buttons
import constants

import creatures
import creature_states
import game_control
import game_states
import iso_grid
import sprites
import sprite_sheet #<UNUSED>
import player
 


#font = pygame.font.SysFont('comicsans', 90, 0, 0)

def load_image(file):
    "loads an image, prepares it for play"
    try:
        surface = pygame.image.load(file).convert()
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs
        

def Draw_Text(text, x, y, surface):
    label = font.render(text, 1, (75,25,0))
    surface.blit(label, (x, y))

def Draw_Window(surface):
    surface.fill((0,80,80))



def main():
    # SETUP ///////////////////////////////////////////////////////////////////    

    #game_control.Game.init()
    game = game_control.Game
    game.init() 


    # Give the player some creatures (change to player buys creatures)
    #player.roster_add(['chaos', creatures.ChaosCreature()],
    #                 ['air', creatures.AirCreature()])   
    

    # GAME LOOP ///////////////////////////////////////////////////////////////
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)


        #game_control.Game.update()
        game.update()


        #game_control.Game.curr_state.draw(win)
        game.curr_state.draw(win)

        '''
        lst = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]
        for tup in lst:
            game_states.iso_to_cart(tup)
        '''


        pygame.display.update()

    pygame.quit()
    quit()



win = pygame.display.set_mode((constants.screen_width, constants.screen_height))


main()
