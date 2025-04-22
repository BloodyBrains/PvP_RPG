"""renderables.py - 
Contains the Renderable abstract base class.  
The Renderable class is the base class for all objects that can be drawn 
to the screen.    
"""

class Renderable:
    """Abstract base class for all drawable objects."""

    def draw(self, surface):
        """Draw the object to the surface."""
        raise NotImplementedError("Subclasses must implement draw method")   