# resource_manager.py
"""Handles image and sound loading as well as functions to
    operate on them
"""

import os

import pygame

import constants


def get_images_from_sheet(sheet, width, height):
    """Takes a sprite sheet and returns a list of individual sprites.
    
    Arguments:
        file {[type]} -- [description]
    """
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


def load_image(file):
    "loads an image, prepares it for play"
    try:
        surface = pygame.image.load(os.path.join(constants.ASSETS, file)).convert()
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs
