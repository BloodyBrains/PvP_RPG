# creatures.py

import abc
import os

import pygame

import constants
import creature_states
import iso_grid
from resource_manager import get_images_from_sheet


SPRITE_W = 96
SPRITE_H = 80

SPEED = 4


class Creature(abc.ABC, pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), sprite_sheet=None):
        super().__init__()
        self.pos = pos
        self.iso_pos = None # tuple position with respect to the isometric
                            # battle grid
        self.width = 0 #sprite height
        self.height = 0 #sprite height
        self.grid_offset = ((constants.TILE_W_HALF - (self.width / 2), (constants.TILE_H_HALF - self.height))) # The offset needed to center the sprite on a grid tile
        self.move_amount = 3 # number of tiles the player can move
        self.speed_x = 0
        self.image = None
        self.rect = pygame.Rect((self.pos), (SPRITE_W, SPRITE_H))
        self.speed = 0
        self.ap = 0
        self.actions = {} #dict of all actions owned by agent
        self.action = None # str ID of the current action being taken
        self.valid_actions = [] #list of action ids the agent can currently perform
        self.turn_state = 'init' # dictates the phase of the active agents turn
                                 #      init, update, finish
        #self.requirements = {} # ['req' : quantity]

        #----------------------------------------------------------------------------------------------------
        if sprite_sheet is None:
            self.sprites = {}
        else:
            self.sprites = get_images_from_sheet(sprite_sheet, SPRITE_W, SPRITE_H)
            self.animations = {}
            self.animations['idle'] = [self.sprites[0], self.sprites[3]]
            self.animations['attack'] = [self.sprites[1]]
            self.animations['hurt'] = [self.sprites[3]]
            self.animations['die'] = [self.sprites[2]]
            self.animations['move'] = [self.sprites[0], self.sprites[3]] 


    def __str__(self):
        return self.name

    # unused
    def update(self, cam_offset):
        # Handle position adjustment for camera movement
        # TO DO: Maybe do this in the creature state?
        #   I don't like calling creature.update() and creature.run_state()
        x = self.pos[0] + cam_offset[0]
        y = self.pos[1] + cam_offset[1]
        self.rect.move(x, y)

    def draw(self, surface):
        surface.blit(self.state.animation[self.state.curr_frame], 
                     self.pos)

    def draw_action(self, surface):
        """Calls the draw method for the current action being taken
        """
        if self.action is not None:
            self.actions[self.action].draw(surface)

    def reset_turn(self):
        if self.action is not None:
            self.actions[self.action].reset()
            self.action = None

    def start_action(self, action_id):
        self.action = action_id
        self.actions[self.action].start()

    @abc.abstractmethod
    def on_event(self, event): pass

    @abc.abstractmethod
    def run_state(self): pass

    @abc.abstractmethod
    def take_turn(self, action): pass        
            


class ChaosCreature(Creature):
    '''
    sprites = get_images_from_sheet('chaos.png', SPRITE_W, SPRITE_H)
    animations = {}
    animations['idle'] = [sprites[0], sprites[3]]
    animations['attack'] = [sprites[1]]
    animations['hurt'] = [sprites[3]]
    animations['die'] = [sprites[2]]
    animations['move'] = [sprites[0], sprites[3]]
    '''
    requirements = {}
    requirements['red'] = 1

    # Creature Info
    species = 'lumox'
    age = 0


    def __init__(self, pos=(0, 0), sprite_sheet=None):
        super().__init__(pos, sprite_sheet)
        self.name = 'chaos'
        self.width = self.animations['idle'][0].get_width()
        self.height = self.animations['idle'][0].get_height()
        self.anim_speed = 8 #Num of game render cycles between animation frames
                            #   at 30 FPS
        self.states = {}
        self.states['idle'] = creature_states.IdleState(self.animations['idle'],
                                                        self.anim_speed)
        self.states['attack'] = creature_states.IdleState(self.animations['attack'],
                                                          self.anim_speed)
        self.states['hurt'] = creature_states.IdleState(self.animations['hurt'],
                                                        self.anim_speed)
        self.states['die'] = creature_states.IdleState(self.animations['die'],
                                                       self.anim_speed)
        self.states['moving'] = creature_states.Moving(self.animations['move'],
                                                        self.anim_speed)
        self.state = self.states['idle']

        self.speed = 5
        self.ap = self.speed

    #def update(self): pass

    #def draw(self, surface): pass

    def on_event(self, event):
        temp = self.states[self.state.on_event(event)]
        if temp != self.state:
            self.prev_state = self.state
            self.state = temp

        del temp

    def run_state(self):
        val = self.state.run()
        if val is not None:
            self.on_event(val)

    def take_turn(self, action):
        pass


class AirCreature(Creature):
    '''
    sprites = get_images_from_sheet('air.png', SPRITE_W, SPRITE_H)
    animations = {}
    animations['idle'] = [sprites[0], sprites[3]]
    animations['attack'] = [sprites[1]]
    animations['hurt'] = [sprites[3]]
    animations['die'] = [sprites[2]]
    animations['move'] = [sprites[0], sprites[3]]
    '''
    requirements = {}
    requirements['white'] = 1

    species = 'octo'

    def __init__(self, pos=(0, 0), sprite_sheet=None):
        super().__init__(pos, sprite_sheet)
        self.name = 'air'
        self.width = self.animations['idle'][0].get_width()
        self.height = self.animations['idle'][0].get_height()
        self.anim_speed = 8 #Num of game render cycles between animation frames
                            #   at 30 FPS
        self.states = {}
        self.states['idle'] = creature_states.IdleState(self.animations['idle'],
                                                        self.anim_speed)
        self.states['attack'] = creature_states.IdleState(self.animations['attack'],
                                                          self.anim_speed)
        self.states['hurt'] = creature_states.IdleState(self.animations['hurt'],
                                                        self.anim_speed)
        self.states['die'] = creature_states.IdleState(self.animations['die'],
                                                       self.anim_speed)
        self.states['move'] = creature_states.Moving(self.animations['move'],
                                                                self.anim_speed)
        self.state = self.states['idle']

        self.speed = 10
        self.ap = self.speed

    #def update(self): pass

    #def draw(self, surface): pass

    def on_event(self, event):
        temp = self.states[self.state.on_event(event)]
        if temp != self.state:
            self.prev_state = self.state
            self.state = temp

        del temp

    def run_state(self):
        val = self.state.run()
        if val is not None:
            self.on_event(val)

    def take_turn(self, action):
        pass
    

