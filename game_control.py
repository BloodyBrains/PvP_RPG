# game_control.py
import assets
import game_states
import player

class Game():
    states = {}
    curr_state = None
    #player1 = None
    #player2 = None

    @staticmethod
    def init():
        assets.load_assets()

        # Init the player, they must be persistent throughout all game states
        player1 = player.Player(sprite_sheet=assets.player_sprites['player'])
        player2 = player.Player(sprite_sheet=assets.player_sprites['player'])

        Game.states.update(
            {'start_screen':game_states.StartScreen(assets.startstate_sprites),
             'roster_edit':game_states.RosterEdit(assets.rosteredit_sprites, player1, player2),
             'battle_screen':game_states.BattleScreen(assets.battlestate_sprites, player1, player2)}
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