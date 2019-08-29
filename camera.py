# camera.py

import constants
import events

class Camera:
    def __init__(self, event_manager):
        self.ev_mgr = event_manager
        event_manager.register_listener(self)
        self.pos = (0, 0)
        

    def notify(self, event):
        pass
                
    def update(self):
        x = self.pos[0] + self.x_speed
        y = self.pos[1] + self.y_speed
        self.pos = (x, y)


    def center(self, position):
        """Centers the camera on the position
        
            Arguments:
                position {tuple(int)} -- position to center on
        """        
        x = (constants.SCREEN_WIDTH / 2) - position[0]
        y = (constants.SCREEN_HEIGHT / 2) - position[1]
        offset = (x, y)
        camx = self.pos[0] - x
        camy = self.pos[1] - y
        self.pos = (camx, camy)
        ev = events.CameraMove(offset)
        self.ev_mgr.post(ev)


    # Initial values of the offset. Changes when the cam moves
    offset_x = constants.CAM_STARTX
    offset_y = constants.CAM_STARTY

    x_speed = 0
    y_speed = 0    