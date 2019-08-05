# resource_manager.py
"""Handles image and sound loading as well as functions to
    operate on them
"""

import pygame

def get_images_from_sheet(file, width, height):
    """Takes a sprite sheet and returns a list of individual sprites.
    
    Arguments:
        file {[type]} -- [description]
    """
    sheet = pygame.image.load(file)
    sprites = []
    dest_rect = pygame.Rect((0, 0), (width, height))
    total = sheet.get_width() / width
    i = 0
    while i < total:
        image = pygame.Surface((width, height))
        image.blit(sheet, (0,0), ((width * i), 0, width, height))
        image.set_colorkey((0,0,0))
        sprites.append(image)
        i += 1

    return sprites
