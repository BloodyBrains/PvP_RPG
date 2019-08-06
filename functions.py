# functions.py
""" A group of commonly used functions
"""

import camera
import constants

def iso_to_cart(iso_pos, width=0, height=0, with_offset=0):
    """Takes an isometric grid position and returns the screen coords
            of the top-left corner of the tile.
        If width, height args are passed, they are used to center a
            sprite on the tile
    
    Arguments:
        iso_pos {(int, int)} -- isometric grid postion to convert
        width {int} ----------- width of image to be centered on tile
        height {int} ---------- height of image to be centered on tile
    """
    # set creature pos to top-left corner of tile
    #<TO DO: factor this: width(x + y)
    cart_x = (iso_pos[0] * constants.TILE_W_HALF) + (iso_pos[1] * constants.TILE_W_HALF)
    cart_y = (iso_pos[1] * constants.TILE_H_HALF) - (iso_pos[0] * constants.TILE_H_HALF)

    # If we need the camera offset
    if with_offset != 0:
        cart_x += camera.offset_x
        cart_y += camera.offset_y

    # adjust position based on sprite size relative to center of tile
    # TO DO: adjust y pos to be slightly below center
    if not(width and height) == 0:
        cart_x += (constants.TILE_W_HALF - (width / 2))
        cart_y += (constants.TILE_H_HALF - height)

    '''
    # if we need the camera offset
    if not(with_offset) == False:
        cart_x = cart_x + cls.cam_offset_x + iso_grid.IsoGrid.start_x
        cart_y = cart_y + cls.cam_offset_y + iso_grid.IsoGrid.start_y    '''

    return (cart_x, cart_y)