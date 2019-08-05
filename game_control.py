# game_control.py

import game_states
import player

class Game():
    states = {}
    curr_state = None
    player1 = None
    player2 = None

    @staticmethod
    def init():
        Game.states.update(
            {'start_screen':game_states.StartScreen(),
             'roster_edit':game_states.RosterEdit(),
             'battle_screen':game_states.BattleScreen()}
        )

        try:
            Game.curr_state = Game.states['start_screen']
        except IndexError:
            print("idiot")

    @staticmethod       
    def update():
        new_state = None
        new_state = Game.curr_state.update()
        if new_state is not None:
            Game.curr_state = Game.states[new_state]
            print("new ", Game.curr_state)
            Game.curr_state.on_enter()

    @staticmethod
    def draw():
        Game.curr_state.draw()