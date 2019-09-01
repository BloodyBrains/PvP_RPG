# player.py
from collections import OrderedDict
import math

import assets
import creatures
import actions
import creature_states # _HACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import game_states 
from resource_manager import get_images_from_sheet


# TO DO: check for roster_add invalid parameters

SPRITE_W = 96
SPRITE_H = 80

SPEED = 4

class Player(creatures.Creature):   

    def __init__(self, name, pos=(0, 0), sprite_sheet=None):
        super().__init__(name, pos, sprite_sheet)
        self.roster = OrderedDict() # dict of all creatures owned
        self.roster_ids = [] # list of creature id's only
        self.party = {} # dict of creatures in the active party
        self.summons_available = [] # list of creatures available for summoning
        self.requirements = {} # dict of earned requirements for summoning. ['req' : quantity]
        #self.name = 'player1'

        '''
        sprites = get_images_from_sheet(assets.player_sprites['player'], SPRITE_W, SPRITE_H)    
        self.animations = {}
        self.animations['idle'] = [sprites[1], sprites[4]]
        self.animations['attack'] = [sprites[2]]
        self.animations['hurt'] = [sprites[4]]
        self.animations['die'] = [sprites[3]]
        self.animations['move'] = [sprites[1], sprites[4]]

        self.animations = {}
        self.anim_speed = 8 #Num of game render cycles between animation frames
                            #   at 30 FPS
        '''
        self.states = {}
        self.states['idle'] = creature_states.IdleState(self.animations['idle'],
                                                        self.anim_speed)
        self.states['attack'] = creature_states.AttackState(self.animations['attack'],
                                                          self.anim_speed)
        #self.states['hurt'] = creature_states.HurtState(self.animations['hurt'],
        #                                                self.anim_speed)
        self.states['die'] = creature_states.DieState(self.animations['die'],
                                                       self.anim_speed)
        self.states['moving'] = creature_states.Moving(self.animations['move'],
                                                        self.anim_speed)
        self.state = self.states['idle']

        #self.width = self.animations['idle'][0].get_width()
        #self.height = self.animations['idle'][0].get_height()

        self.speed = 5
        self.ap = self.speed
        
        #self.actions['move'] = actions.Move(self)
        #self.actions = {} #List of action.ids the agent owns
        action_hooks = {'move': actions.HOOKS['move']}
        self.add_actions(action_hooks)
        #self.valid_actions = [] #List of actions the agent can currently perform

        # Give the player some creatures. Change later!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.requirements['red'] = 1
        self.requirements['white'] = 1
        self.roster_add(['chaos', creatures.ChaosCreature(sprite_sheet=assets.chaos_sprites['chaos'])],
                        ['air', creatures.AirCreature(sprite_sheet=assets.air_sprites['air'])])


    def on_event(self, event):
        temp = self.states[self.state.on_event(event)]
        if temp != self.state:
            self.prev_state = self.state
            self.state = temp


    def run_state(self):
        val = self.state.run()
        if val is not None:
            self.on_event(val)

    def roster_add(self, *id_instance):
        """Takes a variable number of ['id', creatures.Creature()] list args
                and adds them to the player roster dict
            Also appends the id to the roster_ids list
        """
        for elem in id_instance:
            self.roster[elem[0]] = elem[1]
            self.roster_ids.append(elem[0])
            print(self.roster)

    def turn_init(self):
        """Assembles the agents valid_actions list
        """
        # Assess the current state of the battle
        # Assemble valid_actions list
        # Assemble BattleScreen.turn_menu
        # Set turn_state to 'update'

        # check if new summons are available
        '''
        for creature in self.roster.values():
            for item in creature.requirements.items():
                if self.requirements[item[0]] >= item[1]:
                    self.summon_add(agent)
        '''

        # Check for action reqs; assemble valid_actions list
        self.valid_actions = []
        #for action in self.actions.values():
        #    if action.check_reqs():
        #        self.valid_actions.append(action.ID)
        self.check_action_reqs()

        # assemble turn menu from valid_actions
        #game_states.BattleScreen.make_turn_menu(self.valid_actions) #TO DO: this is ugly

    def take_turn(self):
        if self.action is not None:
            self.actions[self.action].run()
        # update logic
        # update turn menu
        # set turn_state to 'finish'
        
    def add_actions(self, action_hooks):
        self.actions.update(action_hooks) 

    def check_action_reqs(self):
        for action in self.actions:
            if self.actions[action](self):
                self.valid_actions.append(action)

    def summon_add(self, *summon_ids):
        for elem in summon_ids:
            self.summons_available.append(elem)


    def get_roster_thumbs(self, id):
        """Returns first frame of Creature.animations['idle'] for the
            creature with the matching id.
        
        Arguments:
            id {<str>name} -- key for player.roster dict
        """
        return self.roster[id].animations['idle'][0]

    def summon(self): pass    

    # NOT IMPLEMENTED
    def get_roster_ids(self, num): 
        if num > len(roster):
            num = len(roster)
        elif num < 0:
            num = 0

        #id = list(roster.keys())[num]
        #return id        


#player1 = Player()
#player2 = Player()


    