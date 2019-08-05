# sprite_sheet.py

import pygame

class Sprite_Sheet:

    def __init__(self, file_name):
        """Returns a pygame.Surface called sprite_sheet"""
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite_sheet.set_colorkey((0,0,0))
        # Create a list to store individual sprites
        self.sprites = []
        
    def get_image(self, top_left_x, top_left_y, sprite_width, sprite_height):
        """Returns a sprite from the sprite_sheet as a pygame.Surface from 
                the specified rect coords
        
        Arguments:
            top_left_x {int} -- x position of top left corner relative to sprite_sheet
            top_left_y {int} -- [description]
            sprite_width {int} -- [description]
            sprite_height {int} -- [description]
        """
        image = pygame.Surface([sprite_width, sprite_height])
        image.blit(self.sprite_sheet, (0,0), (top_left_x, top_left_y, sprite_width, sprite_height))
        image.set_colorkey((0,0,0))
        return image