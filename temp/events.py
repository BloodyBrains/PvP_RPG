import pygame

import borg
import camera
import constants


class Event:
    """Superclass for events
    """
    def __init__(self, name='generic'):
        self.name = name


class EventManager(borg.Borg):
    def __init__(self):
        super().__init__()

        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary() #Use this so unused listeners will be auto unregistered

    #----------------------------------------------------------------------
    def register_listener(self, listener):
        self.listeners[ listener ] = 1

    #----------------------------------------------------------------------
    def unregister_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]

    #----------------------------------------------------------------------
    def post(self, event):
        for listener in self.listeners.keys():
            #NOTE: If the weakref has died, it will be 
            #automatically removed, so we don't have 
            #to worry about it.
            listener.Notify( event )

    def get_events(self):
        #CHECK FOR EVENTS------------------------------------------------------------------
        for event in pygame.event.get():
            #Check for QUIT
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                raise SystemExit

            #Check for Keys---------------------------------------------------
            if event.type == pygame.KEYDOWN:
                #Check for Arrow Keys
                if event.key == pygame.K_LEFT:
                    camera.x_speed = constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_x = constants.CAM_SPEED
                elif event.key == pygame.K_RIGHT:
                    camera.x_speed = -constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_x = -constants.CAM_SPEED

                if event.key == pygame.K_UP:
                    camera.y_speed = constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_y = constants.CAM_SPEED
                elif event.key == pygame.K_DOWN:
                    camera.y_speed = -constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_y = -constants.CAM_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    camera.x_speed = 0
                    iso_grid.IsoGrid.velocity_x = 0
                elif event.key == pygame.K_RIGHT:
                    camera.x_speed = 0
                    iso_grid.IsoGrid.velocity_x = 0

                if event.key == pygame.K_UP:
                    camera.y_speed = 0
                    iso_grid.IsoGrid.velocity_y = 0
                elif event.key == pygame.K_DOWN:
                    camera.y_speed = 0
                    iso_grid.IsoGrid.velocity_y = 0