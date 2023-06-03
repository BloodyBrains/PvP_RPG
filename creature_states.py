# creature_states.py
import abc

import constants
from functions import iso_to_cart


class State:
    @abc.abstractmethod
    def on_event(self, event):
        """Called to switch states
        
        Arguments:
            event {str} -- the state to switch to
        """        
        pass

    @abc.abstractmethod
    def run(self):
        """Contains the update logic
        """
        pass

    @abc.abstractmethod
    def on_enter(self, **kwarg):
        """Called when state is entered to perform setup logic
        """
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class IdleState(State):
    def __init__(self, animation, anim_speed, owner):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
        self.owner = owner
        self.curr_frame = 0

    def on_enter(self): pass

    def run(self):
        if self.anim_timer == self.anim_speed:
           self.curr_frame = (self.curr_frame + 1) % len(self.animation)
           self.anim_timer = 0
        elif self.anim_timer < self.anim_speed:
            self.anim_timer += 1

    def on_event(self, event):
        if event == 'attack':
            return 'attack'

        if event == 'die':
            return 'die'

        if event == 'move':
            return 'move'

    
class AttackState(State):
    def __init__(self, animation, anim_speed, owner):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
        self.owner = owner
        self.curr_frame = 0

    def on_enter(self): pass

    def run(self):
        if self.anim_timer == self.anim_speed:
           self.curr_frame = (self.curr_frame + 1) % len(self.animation)
           self.anim_timer = 0
           return 'prev'
        elif self.anim_timer < self.anim_speed:
            self.anim_timer += 1


    def on_event(self, event):
        if event == 'prev':
            return 'prev'


class DieState(State):
    def __init__(self, animation, anim_speed, owner):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
        self.owner = owner
        self.curr_frame = 0

    def on_enter(self): pass

    def run(self):
        if self.anim_timer == self.anim_speed:
           self.curr_frame = (self.curr_frame + 1) % len(self.animation)
           self.anim_timer = 0
        elif self.anim_timer < self.anim_speed:
            self.anim_timer += 1


    def on_event(self, event):
        if event == 'prev':
            return 'prev'

class Moving(State):
    def __init__(self, animation, anim_speed, owner):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
        self.owner = owner
        self.curr_frame = 0
        self.dest = None
        self.direction1 = 1
        self.direction2 = 1

    def on_enter(self, iso_dest):
        self.dest = iso_dest
        self.first_pos = (iso_dest[0], self.owner.iso_pos[1])
        self.distance1 = abs(self.owner.iso_pos[0] - self.first_pos[0]) * constants.TILE_W_HALF
        self.distance2 = abs(self.first_pos[1] - self.dest[1]) * constants.TILE_W_HALF
        if self.owner.iso_pos[0] > self.first_pos[0]:
            self.direction1 = -1 # use negative slope
        if self.dest[1] < self.first_pos[1]:
            self.direction2 = -1 # use negative slope
        self.is_row_move = True # Move along the row first.


    def run(self):
        if self.anim_timer == self.anim_speed:
           self.curr_frame = (self.curr_frame + 1) % len(self.animation)
           self.anim_timer = 0
        elif self.anim_timer < self.anim_speed:
            self.anim_timer += 1

        if self.is_row_move:
            if self.distance1 >= constants.MOVE_SPEED:
                x = self.direction1 * (constants.SLOPE_MOVE[0] * constants.MOVE_SPEED)
                y = -(self.direction1 * (constants.SLOPE_MOVE[1] * constants.MOVE_SPEED))
                self.owner.rect.move_ip(x, y)
                self.owner.pos = self.owner.rect.topleft
                self.distance1 -= abs(x)
            else:
                print(self.owner.rect.topleft, self.owner.rect.center)
                self.owner.rect.topleft = iso_to_cart(self.first_pos, self.owner.width, self.owner.height)
                print(self.owner.rect.topleft, self.owner.rect.center)
                self.owner.pos = self.owner.rect.topleft
                self.is_row_move = False
        else:
            if self.distance2 >= constants.MOVE_SPEED:
                x = self.direction2 * (constants.SLOPE_MOVE[0] * constants.MOVE_SPEED)
                y = self.direction2 * (constants.SLOPE_MOVE[1] * constants.MOVE_SPEED)
                self.owner.rect.move_ip(x, y)
                self.owner.pos = self.owner.rect.topleft
                self.distance2 -= abs(x)
            else:
                print(self.owner.rect.topleft, self.owner.rect.center)
                self.owner.rect.topleft = iso_to_cart(self.dest, self.owner.width, self.owner.height)
                print(self.owner.rect.topleft, self.owner.rect.center)
                self.owner.pos = self.owner.rect.topleft
                self.owner.iso_pos = self.dest
                # return 'prev'
                self.owner.end_action()        

    def on_event(self, event):
        if event == 'prev':
            return 'prev'


#unused
class ActiveTurnState(State):
    def __init__(self):
        #
        pass
    '''
    def __init__(self, animation, anim_speed, owner):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
        self.owner = owner
        self.curr_frame = 0

    def run(self):
        if self.anim_timer == self.anim_speed:
           self.curr_frame = (self.curr_frame + 1) % len(self.animation)
           self.anim_timer = 0
           return 'prev'
        elif self.anim_timer < self.anim_speed:
            self.anim_timer += 1

    def on_event(self, event):
        if event == 'prev':
            return 'prev'
    '''