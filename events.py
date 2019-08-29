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
    def register_listener(self, listener, event_types=None):
        """Registers the listener with the event_manager.
        
        Arguments:
            listener {class instance} -- Must implement notify()
        
        Keyword Arguments:
            event_types {list[int]} -- List of all event types to listen for (default: {(constants.EV_NONE)})
        """
        if event_types is None: event_types = [constants.EV_NONE]
        self.listeners[ listener ] = event_types

    #----------------------------------------------------------------------
    def unregister_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]

    #----------------------------------------------------------------------
    def post(self, event):
        #self.listeneres = {k:v for k,v in self.listeners.items() if v}
        for listener in list(self.listeners): # PYTHON 3 HACK!!!!!!!!!!!!!!!!
            #NOTE: If the weakref has died, it will be 
            #automatically removed, so we don't have 
            #to worry about it.
            if self.listeners[listener]:
                if event.id in self.listeners[listener]:
                    stop = listener.notify(event)
                    if stop:
                        break
            else:
                self.listeners.pop(listener)

    def get_events(self):
        #CHECK FOR EVENTS------------------------------------------------------------------
        for event in pygame.event.get():
            ev = ''
            #Check for QUIT
            if event.type == pygame.QUIT:
                ev = QuitEvent()
                self.post(ev)
                return 

            #Check for Keys---------------------------------------------------
            if event.type == pygame.KEYDOWN:
                #Check for Arrow Keys
                if event.key == pygame.K_LEFT:
                    ev = KeyDown(constants.EV_KEY_LEFT)
                    self.post(ev)
                    break
                    #camera.x_speed = constants.CAM_SPEED
                    #iso_grid.IsoGrid.velocity_x = constants.CAM_SPEED
                elif event.key == pygame.K_RIGHT:
                    ev = KeyDown(constants.EV_KEY_RIGHT)
                    self.post(ev)
                    break
                    #camera.x_speed = -constants.CAM_SPEED
                    #iso_grid.IsoGrid.velocity_x = -constants.CAM_SPEED

                if event.key == pygame.K_UP:
                    ev = KeyDown(constants.EV_KEY_UP)
                    self.post(ev)
                    break
                    #camera.y_speed = constants.CAM_SPEED
                    #iso_grid.IsoGrid.velocity_y = constants.CAM_SPEED
                elif event.key == pygame.K_DOWN:
                    ev = KeyDown(constants.EV_KEY_DOWN)
                    self.post(ev)
                    break
                    #camera.y_speed = -constants.CAM_SPEED
                    #iso_grid.IsoGrid.velocity_y = -constants.CAM_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    ev = KeyUp(constants.EV_KEY_LEFT_UP)
                    self.post(ev)
                    break
                    #camera.x_speed = 0
                    #iso_grid.IsoGrid.velocity_x = 0
                elif event.key == pygame.K_RIGHT:
                    ev = KeyUp(constants.EV_KEY_RIGHT_UP)
                    self.post(ev)
                    break
                    #camera.x_speed = 0
                    #iso_grid.IsoGrid.velocity_x = 0

                if event.key == pygame.K_UP:
                    ev = KeyUp(constants.EV_KEY_UP_UP)
                    self.post(ev)
                    break
                    #camera.y_speed = 0
                    #iso_grid.IsoGrid.velocity_y = 0
                elif event.key == pygame.K_DOWN:
                    ev = KeyUp(constants.EV_KEY_DOWN_UP)
                    self.post(ev)
                    break
                    #camera.y_speed = 0
                    #iso_grid.IsoGrid.velocity_y = 0

            # Check for clicks------------------------------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ev = MouseEvent(pos)
                self.post(ev)
                break


class AgentClick(Event):
    def __init__(self, agent_id):
        self.id = agent_id

class KeyDown(Event):
    def __init__(self, key_id):
        self.id = key_id


class KeyUp(Event):
    def __init__(self, key_id):
        self.id = key_id


class MouseEvent(Event):
    def __init__(self, mouse_pos):
        self.pos = mouse_pos
        self.id = constants.EV_MOUSE_CLICK

class CameraMove(Event):
    def __init__(self, offset):
        """Triggered when camera is moved by means other than pressing arrow keys.
        
        Arguments:
            Event {class} -- base class for all events
            offset {tuple(int)} -- change in cam.pos (x, y)
        """
        self.id = constants.EV_CAM_MOVE
        self.offset = offset
        
class QuitEvent(Event):
    """
    Quit event.
    """    
    def __init__(self):
        self.id = constants.EV_QUIT