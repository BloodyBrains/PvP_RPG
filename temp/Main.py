"""Contains the main loop and creates the Game instance.
"""

import pygame

import assets
import constants
import game_mgr


pygame.init()
win = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

def main():
    clock = pygame.time.Clock()
    
    game_mgr.init()

    while game_mgr.running:
        clock.tick(30)

        game_mgr.update()

        game_mgr.draw(win)

        pygame.display.update()


    pygame.quit()
    quit()


main() #GAME STARTS HERE
