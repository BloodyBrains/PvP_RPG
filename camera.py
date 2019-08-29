# camera.py

import constants
import events

class Camera:
    def __init__(self, event_manager):
        self.ev_mgr = event_manager
        event_manager.register_listener(self)
        self.pos = (0, 0)
        self.x_speed = 0
        self.y_speed = 0
        

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
        cam_x = position[0] - (constants.SCREEN_WIDTH / 2)
        cam_y = position[1] - (constants.SCREEN_HEIGHT / 2)
        self.pos = (cam_x, cam_y)


    # Initial values of the offset. Changes when the cam moves
    #offset_x = constants.CAM_STARTX
    #offset_y = constants.CAM_STARTY

    #x_speed = 0
    #y_speed = 0    