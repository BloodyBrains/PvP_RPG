# game_states.py
import abc
import math

import pygame

import actions
from buttons import Button # _HACK!!! avoids name conflict with <GameState>.buttons attribute
import camera
import constants
import creatures
from functions import iso_to_cart
import iso_grid
import player



class GameState(abc.ABC):
    @abc.abstractmethod
    def update(self): pass

    @abc.abstractmethod
    def draw(self): pass

    @abc.abstractmethod
    def on_enter(self): pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class StartScreen(GameState):
    """State to handle update and and render logic when the
        start screen is active
    """

    bgr = pygame.image.load('start_screen_bgr.png')
    buttons = {}
    buttons['play'] = Button('play_button', 
                             pygame.image.load('play_button.png'))
    visibles = []
    switch_to_states = []


    @classmethod
    def __init__(cls):
        cls.buttons['play'].pos = [((constants.screen_width / 2) 
                                     - (cls.buttons['play'].sprite.get_width() / 2)),
                                    (constants.screen_height / 2)]
        cls.buttons['play'].rect = pygame.Rect(cls.buttons['play'].pos,
                                               (cls.buttons['play'].rect.width,
                                                cls.buttons['play'].rect.height))
        asdf = [cls.buttons['play'].sprite, cls.buttons['play'].pos]
        cls.visibles.append(asdf)

    @classmethod
    def update(cls):
        cls.switch_to_states = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                raise SystemExit

            # Check if a button has been clicked            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in cls.buttons.values():
                    if button.rect.collidepoint(pos):
                        print(button.id)
                        if button.id == 'play_button':
                            #cls.switch_to_states.append('roster_edit')
                            return 'roster_edit'
                    else:
                        print("not clicked")            

    @classmethod
    def draw(cls, game_win):
        game_win.blit(cls.bgr, (0, 0))

        for i in cls.visibles:
            game_win.blit(i[0], i[1])

    @classmethod
    def on_enter(cls):
        pass        


class RosterEdit(GameState):
    '''Game State for "Creature Edit Screen"'''

    bgr = pygame.image.load('nebula_bgr.png')
    buttons = {}
    buttons['play'] = Button('play_button',
                             pygame.image.load('play_button.png')) 

    offset = 10 # space between sprites in roster rect area
    total_positions = 0
    thumb_positions = [] # list of Rect's for sprite positions in roster rect
    roster_buttons = [] # list creature buttons in roster rect

    # roster_rect is the border that surrounds the creature selection area
    roster_rect_x = math.floor(constants.screen_width * 0.1)
    roster_rect_y = 50
    roster_rect_width = math.floor(constants.screen_width * 0.8)
    roster_rect_height = 222
    roster_rect = pygame.Rect((roster_rect_x,
                               roster_rect_y),
                              (roster_rect_width,
                               roster_rect_height))

    # rect for area where selected creature is drawn
    selected_rect = pygame.Rect(math.floor(constants.screen_width * 0.7),
                                math.floor(constants.screen_height * 0.7),
                                constants.CREATURE_W,
                                constants.CREATURE_H)

    roster = {} # dict of pygame.surfaces for all creatures owned by player
    visibles = [] #<NOT FULLY IMPLEMENTED> list of [surface, pos] of images to render
    selected = None # id of creature currently selected for edit

    @classmethod
    def __init__(cls):
        #cls.roster.update({'chaos':player.roster['chaos'].animations['idle'][1],
        #                   'air':player.roster['air'].animations['idle'][1]})
        cls.set_thumb_positions()
        cls.selected = 'chaos' #_HACK!!!-----------------------------------------
        #vis = [cls.roster[cls.selected], cls.selected_rect.topleft]
        #cls.visibles.append(vis)
        cls.total_positions = math.floor(cls.roster_rect_width
                                         / (constants.CREATURE_W + cls.offset))

        cls.buttons['play'].pos = (
                (0, constants.screen_height - cls.buttons['play'].rect.height))
        
        cls.buttons['play'].rect = pygame.Rect(
                (0, constants.screen_height - cls.buttons['play'].rect.height),
                (cls.buttons['play'].rect.width, cls.buttons['play'].rect.height))

    


    @classmethod
    def set_roster_buttons(cls):
        """Creates buttons for each creature in the player's roster
        """
        i = 0
        for name in player.player1.roster_ids:
            cls.roster_buttons.append(Button(name,
                                             player.player1.get_roster_thumbs(name),
                                             pos=cls.thumb_positions[i],
                                             text=name))
            i += 1

    @classmethod
    def draw_roster_buttons(cls, game_win):
        for button in cls.roster_buttons:
            game_win.blit(button.sprite, button.pos)

    @classmethod
    def on_enter(cls):
        """Called from game_control.py when state is entered to update changes
        """
        cls.set_thumb_positions()
        cls.set_roster_buttons()

    @classmethod
    def set_thumb_positions(cls):
        '''Sets the thumbnail position of all of the players creatures The "roster"'''
        cls.thumb_positions = []
        curr_pos_x = cls.roster_rect.x + cls.offset
        curr_pos_y = cls.roster_rect.y + cls.offset

        i = 0
        while i < cls.total_positions:
            if curr_pos_x < (cls.roster_rect.width
                             + cls.roster_rect.x
                             + constants.CREATURE_W): #_HACK!!!!!!!!!!!!!!!!!!!!!!!!
                cls.thumb_positions.append((curr_pos_x + (constants.CREATURE_W * i),
                                            curr_pos_y))
                i += 1
        

    @classmethod
    def update(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                raise SystemExit

            # Check if a creature has been clicked to edit
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in cls.roster_buttons:
                    if button.rect.collidepoint(pos): 
                        cls.selected = button.id
                        print(cls.selected)
                        break
                    else:
                        print("not clicked")

                for button in cls.buttons.values():
                    if button.rect.collidepoint(pos):
                        print(button.id)
                        if button.id == 'play_button':
                            return 'battle_screen'

    @classmethod
    def draw(cls, game_win):
        game_win.blit(cls.bgr, (0, 0))

        # draw rect that borders "creature edit buttons"
        pygame.draw.rect(game_win, (255, 255, 255), cls.roster_rect, 5)
        pygame.draw.rect(game_win, (255, 255, 255), cls.selected_rect, 5)

        # draw play button 
        game_win.blit(cls.buttons['play'].sprite, cls.buttons['play'].pos)

        #cls.draw_creatures(game_win)
        cls.draw_roster_buttons(game_win)

        # draw selected creature <_HACK!!!!!!!!!!!!!>
        game_win.blit(player.player1.roster[cls.selected].animations['idle'][0],
                      cls.selected_rect.topleft)

        #for i in cls.visibles:
            #game_win.blit(i[0], i[1])


class BattleScreen(GameState):
    bgr = pygame.image.load('nebula_bgr.png')
    tile_selected = pygame.image.load('tile_selected.png')

    # action buttons for the active turn menu
    action_buttons = {}
    turn_action = None # id for the action the active_agent will perform 

    turn_menu = None # menu to display action buttons for active agent

    # battle_positions are relative to the isometric battle grid
    battle_positions = [(0, 0), (4, 5), (5, 5)]  
    player_positions = [(3, 5), (3, 2)] # starting positions for players
    turn_order = [] # list of creature ids in their turn order
    agents = {} # dict of all agents on screen
    active_agent = None # Ref to the creature or other agent whose turn it is 
    selected_agent = None

    cam_speed_x = 0 # Number of pixels cam moves per update call. Set to 0 when
                  #     cam is not moving
    cam_speed_y = 0
    cam_offset_x = 0
    cam_offset_y = 0


    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def update(cls):
        # Test for quit and keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                raise SystemExit

            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera.x_speed = constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_x = constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_x = constants.CAM_SPEED
                elif event.key == pygame.K_RIGHT:
                    camera.x_speed = -constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_x = -constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_x = -constants.CAM_SPEED

                if event.key == pygame.K_UP:
                    camera.y_speed = constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_y = constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_y = constants.CAM_SPEED
                elif event.key == pygame.K_DOWN:
                    camera.y_speed = -constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_y = -constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_y = -constants.CAM_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    camera.x_speed = 0
                    iso_grid.IsoGrid.velocity_x = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_x = 0
                elif event.key == pygame.K_RIGHT:
                    camera.x_speed = 0
                    iso_grid.IsoGrid.velocity_x = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_x = 0

                if event.key == pygame.K_UP:
                    camera.y_speed = 0
                    iso_grid.IsoGrid.velocity_y = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_y = 0
                elif event.key == pygame.K_DOWN:
                    camera.y_speed = 0
                    iso_grid.IsoGrid.velocity_y = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_y = 0

            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cls.cam_speed_x = constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_x = constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_x = constants.CAM_SPEED
                elif event.key == pygame.K_RIGHT:
                    cls.cam_speed_x = -constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_x = -constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_x = -constants.CAM_SPEED

                if event.key == pygame.K_UP:
                    cls.cam_speed_y = constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_y = constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_y = constants.CAM_SPEED
                elif event.key == pygame.K_DOWN:
                    cls.cam_speed_y = -constants.CAM_SPEED
                    iso_grid.IsoGrid.velocity_y = -constants.CAM_SPEED
                    for agent in cls.agents.values():
                        agent.cam_speed_y = -constants.CAM_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    cls.cam_speed_x = 0
                    iso_grid.IsoGrid.velocity_x = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_x = 0
                elif event.key == pygame.K_RIGHT:
                    cls.cam_speed_x = 0
                    iso_grid.IsoGrid.velocity_x = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_x = 0

                if event.key == pygame.K_UP:
                    cls.cam_speed_y = 0
                    iso_grid.IsoGrid.velocity_y = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_y = 0
                elif event.key == pygame.K_DOWN:
                    cls.cam_speed_y = 0
                    iso_grid.IsoGrid.velocity_y = 0
                    for agent in cls.agents.values():
                        agent.cam_speed_y = 0
            

            # Check for clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                '''
                for button in cls.roster_buttons:
                    if button.rect.collidepoint(pos): 
                        cls.selected = button.id
                        print(cls.selected)
                        break
                    else:
                        print("not clicked")

                for button in cls.buttons.values():
                    if button.rect.collidepoint(pos):
                        print(button.id)
                        if button.id == 'play_button':
                            return 'battle_screen'
                '''
                for button in cls.turn_menu.buttons.values():
                    if button.rect.collidepoint(pos):
                        print(button.id)
                        if button.id == 'move':
                            cls.turn_action = button.id     

        cls.cam_offset_x += cls.cam_speed_x
        cls.cam_offset_y += cls.cam_speed_y

        camera.offset_x += camera.x_speed
        camera.offset_y += camera.y_speed

        for agent in cls.agents.values():
            agent.update()
            agent.run_state()

        if cls.turn_menu.show:
            cls.turn_menu.update()

        if cls.active_agent is None:
            agent = cls.turn_order.pop(0)
            cls.active_agent = player.player1.roster[agent]
            cls.turn_order.append(cls.calc_turn_order(1))

        cls.active_agent.take_turn(cls.turn_action)

        #player.player1.take_turn()

        iso_grid.IsoGrid.update()


    @classmethod
    def draw(cls, game_win):
        game_win.blit(cls.bgr, (0, 0))

        iso_grid.IsoGrid.draw_tiles(game_win)

        # draw rectangle on selected agents tile
        # TO DO: create a selected_tile object and update it's pos in update()
        '''
        pos = iso_to_cart(cls.selected_agent.iso_pos)
        pos_x = (pos[0]
                + iso_grid.IsoGrid.start_x
                + cls.cam_offset_x)
        pos_y = (pos[1]
                + iso_grid.IsoGrid.start_y
                + cls.cam_offset_y)
        pos = (pos_x, pos_y)
        game_win.blit(cls.tile_selected, pos)
        '''
        pos = iso_to_cart(cls.selected_agent.iso_pos)
        pos_x = (pos[0] + camera.offset_x)
        pos_y = (pos[1] + camera.offset_y)
        game_win.blit(cls.tile_selected, (pos_x, pos_y))

        # TEMPORARY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # draw valid move tiles for active agent
        offsetx = iso_grid.IsoGrid.start_x + cls.cam_offset_x
        offsety = iso_grid.IsoGrid.start_y + cls.cam_offset_y
        for t in cls.active_agent.valid_moves:
            game_win.blit(actions.Move.tile, (t[0] + offsetx, t[1] + offsety))

        for agent in cls.agents.values():
            agent.draw(game_win)

        if cls.turn_menu.show:
            cls.turn_menu.draw(game_win)

    @classmethod
    def on_enter(cls):
        # Sets the starting positions of all active agents.
        # Calculates the order of the first x amount of turns
        # Initializes turn_order list with two players
        # Sets active_agent to the first agent in turn_order list
        # Instantiates the Turn_Menu

        # set the player's positions to the starting positions
        cls.agents['player1'] = player.player1
        cls.agents['player2'] = player.player2
        player.player1.iso_pos = cls.player_positions[0]
        player.player1.pos = iso_to_cart(player.player1.iso_pos,
                                     player.player1.width,
                                     player.player1.height)

        player.player2.iso_pos = cls.player_positions[1]
        player.player2.pos = iso_to_cart(player.player2.iso_pos,
                                     player.player2.width,
                                     player.player2.height)

        '''
        i = 0
        for creature in player.player1.roster.values():
            if i < len(BattleScreen.battle_positions):
                #creature.rect = BattleScreen.battle_positions[i]
                creature.iso_pos = BattleScreen.battle_positions[i]
                creature.pos = cls.iso_to_cart(creature.iso_pos,
                                        creature.width,
                                        creature.height)
                i += 1
            else: break
        '''

        # Calculate the turn order for the next x amount of turns
        cls.turn_order.extend(cls.calc_turn_order(10))

        # Set the active_agent and append the next turn to the list
        agent = cls.turn_order.pop(0)
        cls.active_agent = cls.agents[agent]
        cls.turn_order.append(cls.calc_turn_order(1))
        cls.selected_agent = cls.active_agent

        # Set the turn menu for the active agent
        cls.turn_menu = TurnMenu()
        #cls.turn_menu.add_buttons('move')

        #cls.active_agent.on_event('move')
        #cls.active_agent.take_turn()

    @classmethod
    def make_turn_menu(cls, items): 
        cls.turn_menu.make(items)        


    # General Purpose Methods -------------------------------------------
    

    @classmethod
    def calc_turn_order(cls, num_turns):
        """Returns the id of the creature with the highest amount
            of action points. In case of a tie, a list of all the
            tied creatures are returned.
        
        Returns:
            [list[str]] -- [holds the id/s of the creature/s whose turn is next]
        """
        turn_orders = [] # list of agent ids in turn order
        ap_list = {}
        for agent in cls.agents.values():
            ap_list[str(agent)] = agent.ap
        '''
        for agent in player.roster.values():
            ap_list[str(agent)] = agent.ap
        '''

        i = 0
        while i < num_turns:
            for agent in cls.agents.values():
                ap_list[str(agent)] = ap_list[str(agent)] + agent.speed
                if ap_list[str(agent)] >= 100:
                    turn_orders.append(str(agent))
                    ap_list[str(agent)] = 0
                    i += 1

        return turn_orders


    def get_active_agent():
        """Returns a ref to the agent whose turn is next
        """

        # Pop an id from the turn_order list
        # Set active_player to a ref of the agent whose id we popped
        # Append turn_order with id returned from calc_turn_order


class TurnMenu:
    button_blank = pygame.image.load('button_turn_menu_blank.png')
    font = pygame.font.SysFont('Arial', 10)
    button_width = button_blank.get_width()
    button_height = button_blank.get_height()
    pos = (100, 370)
    buttons = {}
    show = False #Only rendered when True

    def __init__(self): pass        

    @classmethod
    def make(cls, items):
        cls.buttons = {}
        i = 0
        for item in items:
            cls.buttons[item] = Button(item, 
                                       cls.button_blank, 
                                       (cls.pos[0], cls.pos[1] + (i * cls.button_height)),
                                       item)
            i += 1

        cls.show = True

    @classmethod
    def update(cls):
        '''
        new_x = cls.pos[0] + camera.offset_x
        new_y = cls.pos[1] + camera.offset_y
        cls.pos = (new_x, new_y)

        for button in cls.buttons.values():
            button.update()
        '''
        pass

    @classmethod
    def draw(cls, game_win):
        for button in cls.buttons.values():
            text = cls.font.render(button.id, False, (0, 0, 0))
            game_win.blit(cls.button_blank, button.pos)
            game_win.blit(text, (button.pos[0] + 10, button.pos[1] + 5))


    @classmethod
    def add_buttons(cls, *button_ids):
        for button in button_ids:
            cls.buttons[button] = Button(button,
                                          cls.button_blank,
                                          (0, 0),
                                          button)
            print(cls.buttons)

    def populate(self, valid_actions):
        """Populates the turn_menu with buttons from the valid_actions 
               passed in from the active_player
        
        Arguments:
            valid_actions {list(str)} -- [list of players valid actions]
        """
        pass





