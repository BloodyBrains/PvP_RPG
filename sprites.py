# sprites.py

import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = pygame.Rect(self.image.get_rect())
