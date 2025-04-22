"""backgrounds.py
Contains the Bgr class, which is responsible for drawing the background sprite to the window.
"""

class Bgr:
    def __init__(self, sprite):
        self.sprite = sprite

    def draw(self, game_state, win):
        """Draw the background sprite to the window at the camera position."""
    
        win.blit(self.sprite, (0, 0))

    def __repr__(self):
        return f"Bgr(name={str(self.sprite)})"