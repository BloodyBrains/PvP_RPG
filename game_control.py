# game_control.py
import pygame

import assets
import camera
import constants
import events
import game_states
import player

class Game:

    STATE_START = "start_screen"
    STATE_EDIT = 'roster_edit'
    STATE_BATTLE = 'battle_screen'
    STATES = [
        STATE_START,
        STATE_EDIT,
        STATE_BATTLE
    ]

    def __init__(self, events_manager, clock, game_win, cam):
        self.ev_manager = events_manager
        self.listen_types = [constants.EV_QUIT]
        events_manager.register_listener(self, self.listen_types)
        #self.cam = camera.Camera(events_manager, self)

        self.clock = clock
        self.game_win = game_win
        self.cam = cam

        self.states = {}
        self.curr_state = None

        self.is_running = True

        # LOAD
        assets.load_assets()

        # Init the player, they must be persistent throughout all game states
        self.player1 = player.Player('player1', sprite_sheet=assets.player_sprites['player'])
        self.player2 = player.Player('player2', sprite_sheet=assets.player_sprites['player'])

        self.states = {}

        '''
        self.states.update(
            {'start_screen':game_states.StartScreen(assets.startstate_sprites, self.ev_manager, self),
             'roster_edit':game_states.RosterEdit(assets.rosteredit_sprites, self.player1, self.ev_manager, self),
             'battle_screen':game_states.BattleScreen(assets.battlestate_sprites, self.player1, self.player2, self.ev_manager, self)}
        )
        '''

        try:
            #self.change_state(self.STATE_START)
            #self.curr_state = self.states['start_screen']
            self.curr_state = game_states.StartScreen(assets.startstate_sprites, self.ev_manager, self)
        except IndexError:
            print("idiot")


    def run(self):

        while self.is_running:
            self.clock.tick(30)

            self.update()

            self.draw()

            pygame.display.update()


    def update(self):
        #self.ev_manager.get_events()

        self.curr_state.update()

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
                self.curr_state = game_states.StartScreen(assets.startstate_sprites, self.ev_manager, self)
            elif state_id == self.STATE_EDIT:
                self.curr_state = game_states.RosterEdit(assets.rosteredit_sprites, self.player1, self.ev_manager, self)
            elif state_id == self.STATE_BATTLE:
                self.curr_state = game_states.BattleScreen(assets.battlestate_sprites, self.player1, self.player2, self.ev_manager, self)
        else:
            print("No game state: ", state_id)

        self.curr_state.on_enter()
        print(self.curr_state)
    

    def draw(self):
        self.curr_state.draw(self.game_win)

    def notify(self, event_type):
        """Called from event_manager when an event is registered
        """
        if event_type.id == constants.EV_QUIT:
            self.quit()

    def quit(self):
        self.is_running = False
