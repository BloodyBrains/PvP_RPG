# camera.py
from pygame import KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN

import constants
import events

class Camera:
    def __init__(self):
        #event_manager.register_listener(self)
        self.listen_types = [
            K_DOWN,
            K_LEFT,
            K_RIGHT,
            K_UP
        ]
        self.pos = (0, 0)
        self.x_speed = 0
        self.y_speed = 0
        self.is_active = False

        # TODO: Gets registered when the camera is activated
        #events.register_listener(self, self.listen_types)
        

    def notify(self, event, **event_data):
        #Check for Arrow Keys
        if event_data['event_data'] == KEYDOWN:
            if event == K_LEFT:
                self.x_speed = -constants.CAM_SPEED
            elif event == K_RIGHT:
                 self.x_speed = constants.CAM_SPEED

            if event == K_UP:
                 self.y_speed = -constants.CAM_SPEED
            elif event == K_DOWN:
                self.y_speed = constants.CAM_SPEED

        if event_data['event_data'] == KEYUP:
            if event == K_LEFT:
                self.x_speed = 0
            elif event == K_RIGHT:
                self.x_speed = 0

            if event == K_UP:
                self.y_speed = 0
            elif event == K_DOWN:
                self.y_speed = 0
                
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

    def activate(self):
        self.is_active = True
        events.register_listener(self, self.listen_types)

    def deactivate(self):
        self.is_active = False
        events.unregister_listener(self, self.listen_types)


    # Initial values of the offset. Changes when the cam moves
    #offset_x = constants.CAM_STARTX
    #offset_y = constants.CAM_STARTY

    #x_speed = 0
    #y_speed = 0    