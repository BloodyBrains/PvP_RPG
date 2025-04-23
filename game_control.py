# game_control.py
import pygame
from abc import ABC
import setup

import assets
import camera
import constants
import events
import game_states
import GUI
import iso_grid
import player

class Controller(ABC):

    def notify(self, sender: object, event: str) -> None:
        pass

def get_player_roster():
    thumbs = []
    for agent in Game.player1.roster:
        thumbs.append(Game.player1.get_roster_thumbs(agent))
    return Game.player1.roster, Game.player1.roster_ids, tuple(thumbs)


class Game:
    """
    A singleton class that manages the main game loop and delegates
    to the other game components.
    """
    _instance = None # Singleton flag used to prevent multiple instances

    STATE_START = "start_screen"
    STATE_EDIT = 'roster_edit'
    STATE_BATTLE = 'battle_screen'
    STATES = [
        STATE_START,
        STATE_EDIT,
        STATE_BATTLE
    ]

    state_flag = ''

    listen_types = (pygame.QUIT, 
                    events.EV_CHANGE_GAME_STATE #TODO: GameState changes should be triggered internally
                   )

    player1 = None


    '''Singleton pattern. This class should only be instantiated once.
    Called by Python upon instantiation, before __init__.'''
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.state_flag = ''
            self.is_running = True
            self.ev_manager = events.EventManager()
            events.register_listener(self, Game.listen_types)
            #for i in range(len(self.listen_types)):
            #    events.register_callback(self, self.listen_types[i])

            self.gui = GUI.GUIManager()

            self.clock = pygame.time.Clock()
            #self.game_win = pygame.display.set_mode((constants.SCREEN_WIDTH, 
            #                                         constants.SCREEN_HEIGHT))
            self.game_win = setup.window
            #self.cam = camera.Camera()
            #self.battle_grid = iso_grid.IsoGrid()

            self.states = {}
            self.curr_state = None


            # LOAD
            #assets.load_assets()

            # Init the player, they must be persistent throughout all game states
            Game.player1 = player.Player('player1', sprite_sheet=assets.player_sprites['player'])
            self.player2 = player.Player('player2', sprite_sheet=assets.player_sprites['player'])


            '''
            self.states.update(
                {'start_screen':game_states.StartScreen(assets.startstate_sprites, self.ev_manager, self),
                'roster_edit':game_states.RosterEdit(assets.rosteredit_sprites, self.player1, self.ev_manager, self),
                'battle_screen':game_states.BattleScreen(assets.battlestate_sprites, self.player1, self.player2, self.ev_manager, self)}
            )
            '''

            # Set the initial game state
            try:
                #self.change_state(self.STATE_START)
                #self.curr_state = self.states['start_screen']
                self.curr_state = game_states.StartScreen(Game.STATE_START)
                self.state_flag = Game.STATE_START
            except IndexError:
                print("idiot")


    def run(self):

        while self.is_running:
            self.clock.tick(30)

            self.update()

            self.draw()

            pygame.display.update()



    def update(self):
        # Organize what is to be updated and in what order
        #    depending on the curr game state

        # 1) perform game state testing
        # 2) update event listeners
        # 3) get events
        # 4) post events
        #self.ev_manager.get_events()

        self.ev_manager.update()

        '''
        for event in pygame.event.get():
            if event.type in events.listeners_callback:
                if event.type == pygame.QUIT:
                    self.ev_manager.post(events.QuitEvent())
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    the_list = events.listeners_callback[event.type]
                    for i in the_list:
                        i[1](pygame.mouse.get_pos())
                        #print(listener)
                #if event.type == pygame.U
        '''


        temp = self.curr_state.update()
        if temp != None:
            self.state_flag = temp

        if self.state_flag != self.curr_state.name:
            self.change_state(self.state_flag)

        '''
        new_state = None
        new_state = self.curr_state.update()
        if new_state is not None:
            self.curr_state = self.states[new_state]
            print("new ", self.curr_state)
            self.curr_state.on_enter()
        '''


    def change_state(self, state_id):
        if state_id in self.STATES:
            if state_id == self.STATE_START:
                self.curr_state = game_states.StartScreen(game_states.STATE_START)
            elif state_id == self.STATE_EDIT:
                self.curr_state = game_states.RosterEdit(game_states.STATE_EDIT,
                                                         self.player1.get_roster()
                                                         )
            elif state_id == self.STATE_BATTLE:
                self.curr_state = game_states.BattleScreen(game_states.STATE_BATTLE, self.player1, self.player2, self.gui)
        else:
            print("No game state: ", state_id)

        self.curr_state.on_enter()
        print(self.curr_state)
    

    def draw(self):
        self.curr_state.draw(self.game_win)

    def notify(self, event, **event_data):
        """Called from event_manager when an event is registered
        """
        if event == pygame.QUIT:
            self.quit()
            return

    def quit(self):
        self.is_running = False
