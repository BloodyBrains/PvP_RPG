# game_control.py
import pygame

import assets
import events
import game_states
import player

class Game:

    def __init__(self, events_manager, clock, game_win):
        self.ev_manager = events_manager
        events_manager.register_listener(self)
        self.clock = clock
        self.game_win = game_win

        self.states = {}
        self.curr_state = None

        self.is_running = True


        # LOAD
        assets.load_assets()

        # Init the player, they must be persistent throughout all game states
        self.player1 = player.Player(sprite_sheet=assets.player_sprites['player'])
        self.player2 = player.Player(sprite_sheet=assets.player_sprites['player'])

        self.states.update(
            {'start_screen':game_states.StartScreen(assets.startstate_sprites),
             'roster_edit':game_states.RosterEdit(assets.rosteredit_sprites, self.player1, self.player2),
             'battle_screen':game_states.BattleScreen(assets.battlestate_sprites, self.player1, self.player2)}
        )

        try:
            self.curr_state = self.states['start_screen']
        except IndexError:
            print("idiot")


    def run(self):
        while self.is_running:
            self.clock.tick(30)

            self.update()

            self.draw()

            pygame.display.update()


    def update(self):
        # get_events()

        new_state = None
        new_state = self.curr_state.update()
        if new_state is not None:
            self.curr_state = self.states[new_state]
            print("new ", self.curr_state)
            self.curr_state.on_enter()

    def draw(self):
        self.curr_state.draw(self.game_win)