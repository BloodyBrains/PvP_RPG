# creature_states.py
import abc

# state ////////////////////////////////////////

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
    def __init__(self, animation, anim_speed):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
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

        #return self.__str__()

    
class AttackState(State):
    def __init__(self, animation, anim_speed):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
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
    def __init__(self, animation, anim_speed):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
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

# unused
class Moving(State):
    def __init__(self, animation, anim_speed):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
        self.curr_frame = 0
        self.dest = None

    def on_enter(self, iso_dest):
        pass


    def run(self):
        if self.anim_timer == self.anim_speed:
           self.curr_frame = (self.curr_frame + 1) % len(self.animation)
           self.anim_timer = 0
        elif self.anim_timer < self.anim_speed:
            self.anim_timer += 1

    def on_event(self, event):
        if event == 'prev':
            return 'prev'


#unused
class ActiveTurnState(State):
    def __init__(self, animation, anim_speed):
        self.animation = animation
        self.anim_timer = 0
        self.anim_speed = anim_speed
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
