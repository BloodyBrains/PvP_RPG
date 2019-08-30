# game_states.py
import abc
import math
import os

import pygame

import actions
import assets
from buttons import Button # _HACK!!! avoids name conflict with <GameState>.buttons attribute
import camera
import constants
import creatures
import events
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

    @abc.abstractmethod
    def notify(self, event):
        """Called from events.EventManager.post(). Every class that implements
            this must be registered as a listener with the EventManager.
            The event_handled variable is returned to break the post() loop when necessary  
            
            Arguments:
                event {events.Event} -- [Event instance to handle]
        """
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class StartScreen(GameState):
    """State to handle update and and render logic when the
        start screen is active
    """

    def __init__(self, images, event_manager, game):
        self.bgr = images['bgr']
        self.ev_mgr = event_manager
        event_manager.register_listener(self)
        self.game = game

        self.buttons = {}
        self.buttons['play'] = Button('play_button', images['play'])
        self.buttons['play'].pos = [((constants.SCREEN_WIDTH / 2) 
                                     - (self.buttons['play'].sprite.get_width() / 2)),
                                    (constants.SCREEN_HEIGHT / 2)]
        self.buttons['play'].rect = pygame.Rect(self.buttons['play'].pos,
                                               (self.buttons['play'].rect.width,
                                                self.buttons['play'].rect.height))

        self.visibles = []
        #asdf = [self.buttons['play'].sprite, self.buttons['play'].pos]
        self.visibles.append(self.buttons['play'])


    def update(self):
        for event in pygame.event.get():
            ev = ''
            #Check for QUIT--------------------------------------------------
            if event.type == pygame.QUIT:
                ev = events.QuitEvent()
                self.ev_mgr.post(ev)
                return
            # Check for clicks------------------------------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons.values():
                    if button.rect.collidepoint(pos):
                        if button.ID == 'play_button':
                            self.game.change_state('roster_edit')


    def draw(self, game_win):
        game_win.blit(self.bgr, (0, 0))

        for visible in self.visibles:
            visible.draw(game_win)

    def notify(self, event):
        pass

    def on_enter(self):
        pass        


class RosterEdit(GameState):
    '''Game State for "Creature Edit Screen"'''

    offset = 10 # space between sprites in roster rect area
    
    total_positions = 0
    thumb_positions = [] # list of Rect's for sprite positions in roster rect
    roster_buttons = [] # list creature buttons in roster rect

    # roster_rect is the border that surrounds the creature selection area
    roster_rect_x = math.floor(constants.SCREEN_WIDTH * 0.1)
    roster_rect_y = 50
    roster_rect_width = math.floor(constants.SCREEN_WIDTH * 0.8)
    roster_rect_height = 222
    roster_rect = pygame.Rect((roster_rect_x,
                               roster_rect_y),
                              (roster_rect_width,
                               roster_rect_height))
    total_positions = math.floor(roster_rect_width
                                / (constants.CREATURE_W + offset))

    # rect for area where selected creature is drawn
    selected_rect = pygame.Rect(math.floor(constants.SCREEN_WIDTH * 0.7),
                                math.floor(constants.SCREEN_HEIGHT * 0.7),
                                constants.CREATURE_W,
                                constants.CREATURE_H)
    

    def __init__(self, images, player, event_manager, game):
        self.bgr = images['bgr']
        #cls.roster.update({'chaos':player.roster['chaos'].animations['idle'][1],
        #                   'air':player.roster['air'].animations['idle'][1]})
        self.player = player
        self.selected = 'chaos' # id of creature currently selected for edit
        self.ev_mgr = event_manager
        event_manager.register_listener(self)
        self.game = game
        self.roster = {} # dict of pygame.surfaces for all creatures owned by player
        self.visibles = [] #<NOT FULLY IMPLEMENTED> list of [surface, pos] of images to render
        #vis = [cls.roster[cls.selected], cls.selected_rect.topleft]
        #cls.visibles.append(vis)
        self.thumb_positions = []
        
        self.buttons = {}
        self.buttons['play'] = Button('play_button', images['play'])
        self.buttons['play'].pos = (
                (0, constants.SCREEN_HEIGHT - self.buttons['play'].rect.height))
        
        self.buttons['play'].rect = pygame.Rect(
                (0, constants.SCREEN_HEIGHT - self.buttons['play'].rect.height),
                (self.buttons['play'].rect.width, self.buttons['play'].rect.height))

        self.roster_buttons = [] # list of buttons to edit/view creature stats

        self.set_thumb_positions()    


    def set_roster_buttons(self):
        """Creates buttons for each creature in the player's roster
        """
        i = 0
        for name in self.player.roster_ids:
            self.roster_buttons.append(Button(name,
                                             self.player.get_roster_thumbs(name),
                                             pos=self.thumb_positions[i],
                                             text=name))
            i += 1

    def draw_roster_buttons(self, game_win):
        for button in self.roster_buttons:
            game_win.blit(button.sprite, button.pos)

    def notify(self, event):
        pass

    def on_enter(self):
        """Called from game_control.py when state is entered to update changes
        """
        self.set_thumb_positions()
        self.set_roster_buttons()

    def set_thumb_positions(self):
        '''Sets the thumbnail position of all the players creatures in "roster"'''
        self.thumb_positions = []
        curr_pos_x = self.roster_rect.x + self.offset
        curr_pos_y = self.roster_rect.y + self.offset

        i = 0
        while i < self.total_positions:
            if curr_pos_x < (self.roster_rect.width
                             + self.roster_rect.x
                             + constants.CREATURE_W): #_HACK!!!!!!!!!!!!!!!!!!!!!!!!
                self.thumb_positions.append((curr_pos_x + (constants.CREATURE_W * i),
                                            curr_pos_y))
                i += 1
        

    def update(self):
        for event in pygame.event.get():
            ev_handled = False
            if event.type == pygame.QUIT:
                ev = events.QuitEvent()
                self.ev_mgr.post(ev)
                return
            # Check for clicks----------------------------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if creature has been clicked for editing
                for button in self.roster_buttons:
                    if button.rect.collidepoint(pos): 
                        self.selected = button.ID
                        print(self.selected)
                        ev_handled = True
                        break

                if not ev_handled:
                    # Check if a button has been clicked
                    for button in self.buttons.values():
                        if button.rect.collidepoint(pos):
                            print(button.ID)
                            if button.ID == 'play_button':
                                self.game.change_state('battle_screen')

    def draw(self, game_win):
        game_win.blit(self.bgr, (0, 0))

        # draw rect that borders "creature edit buttons"
        pygame.draw.rect(game_win, (255, 255, 255), self.roster_rect, 5)
        pygame.draw.rect(game_win, (255, 255, 255), self.selected_rect, 5)

        # draw play button 
        game_win.blit(self.buttons['play'].sprite, self.buttons['play'].pos)

        #cls.draw_creatures(game_win)
        self.draw_roster_buttons(game_win)

        # draw selected creature <_HACK!!!!!!!!!!!!!>
        game_win.blit(self.player.roster[self.selected].animations['idle'][0],
                      self.selected_rect.topleft)

        #for i in cls.visibles:
            #game_win.blit(i[0], i[1])


class BattleScreen(GameState):
    bgr = None #pygame.image.load(os.path.join(constants.ASSETS, 'nebula_bgr.png'))
    player1 = None
    player2 = None
    tile_selected = None #pygame.image.load(os.path.join(constants.ASSETS, 'tile_selected.png'))
    tile_selected_pos = (0, 0)

    # action buttons for the active turn menu
    action_buttons = {} 

    turn_menu = None # menu to display action buttons for active agent

    # battle_positions are relative to the isometric battle grid
    battle_positions = [(0, 0), (4, 5), (5, 5)]  
    player_positions = [(3, 5), (3, 2)] # starting positions for players
    turn_order = [] # list of creature ids in their turn order
    agents = {} # dict of all agents on screen
    active_agent = None # the creature or other agent whose turn it is 
    selected_agent = None #agent who is selected


    def __init__(self, images, player1, player2, event_manager, game): 
        self.bgr = images['bgr']
        self.tile_selected = images['tile_selected']
        self.player1 = player1
        self.player2 = player2
        self.ev_mgr = event_manager
        self.listen_types = [
            constants.EV_AGENT_CLICKED,
            constants.EV_CAM_MOVE
        ]
        event_manager.register_listener(self, self.listen_types)
        self.game = game
        self.cam = self.game.cam
        self.internal_state = ''
        self.turn_action = None # Reference to the action the active_agent is performing
        self.cam_speed_x = 0 # Number of pixels cam moves per update call. Set to 0 when
                             #     cam is not moving
        self.cam_speed_y = 0

    def update(self):
        
        #CHECK FOR EVENTS------------------------------------------------------------------
        for event in pygame.event.get():
            #Check for QUIT
            if event.type == pygame.QUIT:
                ev = events.QuitEvent()
                self.ev_mgr.post(ev)
                return
            #Check for Keys---------------------------------------------------
            if event.type == pygame.KEYDOWN:
                #Check for Arrow Keys
                if event.key == pygame.K_LEFT:
                    self.cam.x_speed = -constants.CAM_SPEED
                    #self.iso_grid.x_speed = constants.CAM_SPEED
                    #for agent in self.agents.values():
                    #    agent.x_speed = constants.CAM_SPEED
                elif event.key == pygame.K_RIGHT:
                    self.cam.x_speed = constants.CAM_SPEED
                    #self.iso_grid.x_speed = -constants.CAM_SPEED
                    #for agent in self.agents.values():
                    #    agent.x_speed = -constants.CAM_SPEED

                if event.key == pygame.K_UP:
                    self.cam.y_speed = -constants.CAM_SPEED
                    #self.iso_grid.y_speed = constants.CAM_SPEED
                    #for agent in self.agents.values():
                    #    agent.y_speed = constants.CAM_SPEED               
                elif event.key == pygame.K_DOWN:
                    self.cam.y_speed = constants.CAM_SPEED
                    #self.iso_grid.y_speed = -constants.CAM_SPEED
                    #for agent in self.agents.values():
                    #    agent.y_speed = -constants.CAM_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.cam.x_speed = 0
                    #self.iso_grid.x_speed = 0
                    #for agent in self.agents.values():
                    #    agent.x_speed = 0
                elif event.key == pygame.K_RIGHT:
                    self.cam.x_speed = 0
                    #self.iso_grid.x_speed = 0
                    #for agent in self.agents.values():
                    #    agent.x_speed = 0

                if event.key == pygame.K_UP:
                    self.cam.y_speed = 0
                    #self.iso_grid.y_speed = 0
                    #for agent in self.agents.values():
                    #    agent.y_speed = 0
                elif event.key == pygame.K_DOWN:
                    self.cam.y_speed = 0
                    #self.iso_grid.y_speed = 0
                    #for agent in self.agents.values():
                    #    agent.y_speed = 0
            
        
            # Check for clicks------------------------------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen_pos = pygame.mouse.get_pos() # For clicks on HUD objects relative to camera
                x = screen_pos[0] - self.cam.pos[0] 
                y = screen_pos[1] - self.cam.pos[1]
                pos = (x, y)                        # For clicks on map objects

                click_handled = False

                #for listener in cls.listeners
                
                #Check if game agent is clicked--------------------------
                for agent in self.agents.values():
                    if not click_handled:
                        if agent.rect.collidepoint(pos): 
                            if self.internal_state == 'open':
                                self.selected_agent = agent
                                self.tile_selected_pos = iso_to_cart(self.selected_agent.iso_pos)
                                x = self.tile_selected_pos[0] - self.cam.pos[0]
                                y = self.tile_selected_pos[1] - self.cam.pos[1]
                                self.tile_selected_pos = (x, y)
                                self.cam.center(agent.rect.center)                                
                                if self.selected_agent == self.active_agent:
                                    self.active_agent.turn_init()
                                    self.turn_menu.activate(self.active_agent.valid_actions)
                                    click_handled = True
                                else:
                                    #self.active_agent.reset_turn()
                                    self.turn_menu.deactivate()
                                    #Show agent notecard
                                    click_handled = True
                            else:
                                print('game_state.BattleState has no internal state: ', self.internal_state)
                    else:
                        break
                #-------------------------------------------------------------------------------
            
                '''
                #Check if BattleScreen button is clicked----------------------------------------                
                for button in cls.buttons.values():
                    if button.rect.collidepoint(pos):
                        print(button.id)
                        if button.id == 'play_button':
                            return 'battle_screen'
                #-------------------------------------------------------------------------------
                '''
                
                #Check if turn_menu button is clicked-------------------------------------------
                if not click_handled:
                    if self.turn_menu.is_active:
                        for button in self.turn_menu.buttons.values():
                            if button.rect.collidepoint(screen_pos):
                                '''
                                set the active_agents action to selected action
                                get reference to the action
                                set internal state to action state
                                init the action
                                deactivate turn menu
                                '''
                                self.turn_action = self.active_agent.start_action(button.ID)
                                #self.turn_action.adjust_positions(self.cam.pos)
                                self.turn_action.make_move_buttons()
                                self.turn_menu.deactivate()
                                self.internal_state = 'action'
                                click_handled = True
                                break
                else:
                    break
                #-------------------------------------------------------------------------------

                '''
                # Check for Action clicks------------------------------------------------------
                if not click_handled:
                    if cls.active_agent.action is not None:
                        click_handled = cls.active_agent.actions[cls.active_agent.action].check_click(pos)
                else:
                    break
                #-------------------------------------------------------------------------------
                '''
        #-----------------------------------------------------------------------------------------------


        self.cam.update()
        self.iso_grid.update()
        #x = self.tile_selected_pos[0] - self.cam.x_speed
        #y = self.tile_selected_pos[1] - self.cam.y_speed
        #self.tile_selected_pos = (x, y)
        for agent in self.agents.values():
            agent.update()
            #agent.run_state()

        if self.turn_action is not None:
            self.turn_action.update()
        '''
        #UPDATE ENTITIES---------------------------------------------------------------------
        cls.cam_offset_x += cls.cam_speed_x #TO DO: This is only used to update the tiles
        cls.cam_offset_y += cls.cam_speed_y #           for the camera offset

        # Update camera 
        camera.offset_x += camera.x_speed
        camera.offset_y += camera.y_speed

        # Update Isometric tile grid
        iso_grid.IsoGrid.update()        

        # Update tile_selected position
        x = cls.tile_selected_pos[0] + camera.x_speed
        y = cls.tile_selected_pos[1] + camera.y_speed
        cls.tile_selected_pos = (x, y)

        # Update turn_menu
        if cls.turn_menu.is_active: # active when selected == active
            cls.turn_menu.update()

        # Update agents
        for agent in cls.agents.values():
            # Update positions for camera movement
            x = agent.pos[0] + camera.x_speed
            y = agent.pos[1] + camera.y_speed
            agent.pos = (x, y)
            agent.rect.move_ip(camera.x_speed, camera.y_speed)

            agent.run_state()

        # Update the active agent
        cls.active_agent.take_turn()# were passing cls.turn_action

        # If neccessary, get the next turn, center cam on agent
        if cls.active_agent is None: 
            agent = cls.turn_order.pop(0)
            cls.active_agent = player.player1.roster[agent]
            cls.active_agent.init_turn() 
            cls.selected_agent = cls.active_agent
            cls.tile_selected_pos = iso_to_cart(cls.selected_agent.iso_grid, with_offset=1)
            cls.turn_menu.is_active = True
            cls.turn_order.append(cls.calc_turn_order(1))
        '''

    def draw(self, game_win):
        game_win.blit(self.bgr, (0, 0))

        self.iso_grid.draw_tiles(game_win, self.cam.pos) #How is this working?!!!!!!

        # draw rectangle on selected agents tile
        # TO DO: Wrap this in a class and pass in cam_pos, maybe
        x = self.tile_selected_pos[0] - self.cam.pos[0]
        y = self.tile_selected_pos[1] - self.cam.pos[1]
        game_win.blit(self.tile_selected, (x, y))

        # TO DO: Move this to the actions.Move.draw()
        # draw valid move tiles for active agent
        # draw() call for Actions
        self.active_agent.draw_action(game_win, self.cam.pos)
        '''
        if cls.turn_action is not None:
            cls.active_agent.actions[cls.turn_action].draw(game_win)
        '''
        #for t in cls.active_agent.valid_moves:
        #    game_win.blit(actions.Move.tile, (t[0] + camera.offset_x, t[1] + camera.offset_y))

        for agent in self.agents.values():
            agent.draw(game_win, self.cam.pos)
            #new_rect = pygame.Rect(agent.rect.topleft,
            #                       (agent.width, agent.height))
            #pygame.draw.rect(game_win, (255, 0, 0), new_rect, 1)

        if self.turn_menu.is_active:
            self.turn_menu.draw(game_win)

    def notify(self, event):
        '''
        if isinstance(event, events.CameraMove):
            x = self.iso_grid.pos[0] + event.offset[0]
            y = self.iso_grid.pos[1] + event.offset[1]
            self.iso_grid.pos = (x, y)

            x = self.tile_selected_pos[0] + event.offset[0]
            y = self.tile_selected_pos[1] + event.offset[1]
            self.tile_selected_pos = (x, y)

            for agent in self.agents.values():
                x = agent.pos[0] + event.offset[0]
                y = agent.pos[1] + event.offset[1]
                agent.pos = (x, y)
                agent.rect.move_ip(event.offset)
        '''
        '''
        if isinstance(event, events.CameraMove):
            if self.internal_state == 'open':
                self.selected_agent = self.agents[event.id]
                self.tile_selected_pos = iso_to_cart(self.selected_agent.iso_pos)
                if self.selected_agent == self.active_agent:
                    self.turn_menu.is_active = True
                    stop_checking = True
                    return stop_checking
                else:
                    self.active_agent.reset_turn()
                    self.turn_menu.is_active = False
                    #Show agent notecard
                    stop_checking = True
                    return stop_checking
        '''

    def on_enter(self):
        """State setup. Called when the state is first transitioned to.
        """
        # Sets the starting positions of all active agents.
        # Calculates the order of the first x amount of turns
        # Initializes turn_order list with two players
        # Sets active_agent to the first agent in turn_order list
        # Instantiates the Turn_Menu

        # Instantiate the turn menu
        #self.cam = camera.Camera(self.ev_mgr, self.game)
        self.iso_grid = iso_grid.IsoGrid(self.ev_mgr)
        self.turn_menu = TurnMenu(self.ev_mgr)
        #cls.turn_menu.add_buttons('move')

        # Create the two players
        # set the player's positions to the starting positions
        self.agents['player1'] = self.player1
        self.agents['player2'] = self.player2
        self.player1.iso_pos = self.player_positions[0]
        self.player1.pos = iso_to_cart(self.player1.iso_pos,
                                     self.player1.width,
                                     self.player1.height)
        self.player1.rect = pygame.Rect(self.player1.pos, (self.player1.width, self.player1.height))

        self.player2.iso_pos = self.player_positions[1]
        self.player2.pos = iso_to_cart(self.player2.iso_pos,
                                     self.player2.width,
                                     self.player2.height)
        self.player2.rect = pygame.Rect(self.player2.pos, (self.player2.width, self.player2.height))

        for agent in self.agents.values():
            self.ev_mgr.register_listener(agent, agent.listen_types)

        # Set starting positions of players creatures
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
        self.turn_order.extend(self.calc_turn_order(10))

        # Set the active_agent, selected_agent and selected_tile. 
        # Append the next turn to the list
        # TO DO: Maybe wrap this in a set_active_agent() method
        agent = self.turn_order.pop(0)
        self.active_agent = self.agents[agent]
        self.active_agent.turn_init()
        self.turn_order.append(self.calc_turn_order(1))
        self.turn_menu.activate(self.active_agent.valid_actions)
        self.selected_agent = self.active_agent
        self.tile_selected_pos = iso_to_cart(self.selected_agent.iso_pos)
        self.cam.center(self.selected_agent.rect.center)
        self.turn_menu.is_active = True

        self.internal_state = 'open'

        

        #cls.active_agent.on_event('move')
        #cls.active_agent.take_turn()

    def make_turn_menu(self, items): 
        cls.turn_menu.make(items)        


    # General Purpose Methods -------------------------------------------
    

    def calc_turn_order(self, num_turns):
        """Returns the id of the creature with the highest amount
            of action points. In case of a tie, a list of all the
            tied creatures are returned.
        
        Returns:
            [list[str]] -- [holds the id/s of the creature/s whose turn is next]
        """
        turn_orders = [] # list of agent ids in turn order
        ap_list = {}
        for agent in self.agents.values():
            ap_list[str(agent)] = agent.ap
        '''
        for agent in player.roster.values():
            ap_list[str(agent)] = agent.ap
        '''

        i = 0
        while i < num_turns:
            for agent in self.agents.values():
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
    button_blank = pygame.image.load(os.path.join(constants.ASSETS, 'button_turn_menu_blank.png'))
    font = pygame.font.SysFont('Arial', 10)
    button_width = button_blank.get_width()
    button_height = button_blank.get_height()
    pos = (100, 370)
    buttons = {}
    is_active = False

    def __init__(self, event_manager):
        self.ev_mgr = event_manager
        self.listen_types = [
            constants.EV_MOUSE_CLICK
        ]
        event_manager.register_listener(self)        

    def activate(self, items):
        self.ev_mgr.register_listener(self)
        self.buttons = {}
        i = 0
        for item in items:
            self.buttons[item] = Button(item, 
                                       self.button_blank, 
                                       pos=(self.pos[0], self.pos[1] + (i * self.button_height)),
                                       text=item)
            i += 1

        self.is_active = True

    def deactivate(self):
        self.ev_mgr.unregister_listener(self)
        self.is_active = False


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

    def draw(self, game_win):
        for button in self.buttons.values():
            text = self.font.render(button.ID, False, (0, 0, 0))
            game_win.blit(self.button_blank, button.pos)
            game_win.blit(text, (button.pos[0] + 10, button.pos[1]  + 5))


    def notify(self, event): pass
        


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





