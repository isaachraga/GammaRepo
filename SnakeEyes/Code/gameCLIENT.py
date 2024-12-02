import pygame
import pygame.locals
import pygame.freetype  # Import the freetype module.
from collections import namedtuple
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code import controller
from SnakeEyes.Code import player
from SnakeEyes.Code import car
from SnakeEyes.Code import store
import socket
import pickle



'''
End prev connection
pass information to next location
start new connection


1. Register Inputs
2. Send Inputs
3. Receive Data
4. Render Frame

scene check, store current scene, if scene not equal, change scene




BUGS
-animation is running slow
'''


### TO DO ###

########## GAME ##########
class GameCLIENT:
    ##### Initial Setup #####
    def __init__(self, scene_manager):
        self.pNum = 2
        self.connected = False
        self.charactersInitialized = False
        self.enabledControlls = False
        self.c = ''
        self.assigned = False
        self.scene_manager = scene_manager
        self.screen = scene_manager.screen
        self.move_x =''
        self.move_y=''
        self.readyKey=''
        self.pauseKey=''
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mgame'
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.STORE_INFO_PANEL_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 18)
        self.ALERT_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 30)
        
        #self.clock = pygame.time.Clock()
        self.initialization()
        


    def initialization(self):
        ### Flags and General Game Vars ###
        '''
        self.dt = 0
        self.result = "init"
        self.winScore = Preferences.FINISHLINE_SCORE
        self.lastRound = False
        self.gameOverFlag = False
        self.pause = False
        self.scene = "game"
        self.ready = False
        self.allAlarms = False
        self.police = False
        self.numPlayers = 0
        self.Cars = []
        self.Players = []
        self.statusFlag = False
        self.alarmedStores = 0
        self.testing = False

        self.moveSpeed = 300
        self.roundSkipped = False
        self.storeCollider = pygame.Rect((140, 0, 990, 260)) 
        '''
        self.lastRound = False
        self.statusFlag = False
        self.result = ''
        self.police = False
        self.ready = False
        self.alarmedStores = 0
        self.allAlarms = False
        self.Cars = []
        self.Players = []
        self.Stores = []
        self.player = player.Player()
        self.loadingScreen = pygame.image.load('SnakeEyes/Assets/Environment/Background/Background.png')
        self.badgeSprite = pygame.image.load('SnakeEyes/Assets/Icons/badge.png')
        self.moneySprite = pygame.image.load('SnakeEyes/Assets/Icons/cash.png')
        self.storeInfoPanel = pygame.image.load('SnakeEyes/Assets/Environment/Background/Store_Info_Panel.png')
        self.storeSprites = []
        self.carSprites = []
        self.loadSprites()
        self.character_sprites = {}
        '''
        self.playerReset()
        self.playerLocReset()
        self.storeReset()
        '''
        

    def loadSprites(self):
        s1 = pygame.image.load("SnakeEyes/Assets/Environment/Objects/ABC_Liquor.png")
        self.storeSprites.append(s1)
        s2 = pygame.image.load("SnakeEyes/Assets/Environment/Objects/Perris_Jewels.png")
        self.storeSprites.append(s2)
        s3 = pygame.image.load("SnakeEyes/Assets/Environment/Objects/RX-Express.png")
        self.storeSprites.append(s3)
        s4 = pygame.image.load("SnakeEyes/Assets/Environment/Objects/Slow_Panda.png")
        self.storeSprites.append(s4)

        c1 = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP1.png')
        c1 = pygame.transform.scale(c1, (60,150))
        self.carSprites.append(c1)
        c2 = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP2.png')
        c2 = pygame.transform.scale(c2, (60,150))
        self.carSprites.append(c2)
        c3 = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP3.png')
        c3 = pygame.transform.scale(c3, (60,150))
        self.carSprites.append(c3)
        c4 = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP4.png')
        c4 = pygame.transform.scale(c4, (60,150))
        self.carSprites.append(c4)

    ### Character Sprites ###
    # Helper function to cut up sprite sheets
    def getSpriteFrames(self, sprite_sheet, frame_width, frame_height):
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    # Helper function to convert spritesheet to working sprite
    def makeCharacterSprite(self, path, width, height, fr, flipped=False):
        CharacterState = namedtuple('CharacterState', ['sprite_list', 'frame_rate', 'current_frame', 'current_sprite'])
        current_frame = 0 #current frame of animation
        frame_rate = fr #num of frames sprites are held on
        sprite_sheet = pygame.image.load(path).convert_alpha() #sprite sheet
        if flipped:
            sprite_sheet = pygame.transform.flip(sprite_sheet, True, False)
        sprite_list = self.getSpriteFrames(sprite_sheet, width, height) #cut up sprite sheet
        if flipped:
            sprite_list.reverse()
        current_sprite = sprite_list[current_frame // frame_rate]
        return CharacterState(sprite_list    = sprite_list, 
                              frame_rate     = frame_rate, 
                              current_frame  = current_frame, 
                              current_sprite = current_sprite)

    def initializePlayerSprites(self):        
        # Only initialize the characters being used
        for p in self.Players:
            # Jeff
            if p.character == "jeff":
                self.character_sprites["jeff"] = {}
                self.character_sprites["jeff"]["last_action"] = "forward"
                self.character_sprites["jeff"]["profile"] = "SnakeEyes/Assets/Characters/Profile/Jeff Profile.png"
                self.character_sprites["jeff"]["forward"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/Jeff-Foward.png",
                                                                                    60, 75, 2)
                self.character_sprites["jeff"]["back"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/Jeff-Back.png",
                                                                                55, 75, 2)
                self.character_sprites["jeff"]["right"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/Jeff-RightWalk.png",
                                                                                65, 70, 2)
                self.character_sprites["jeff"]["left"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/Jeff-RightWalk.png",
                                                                                65, 70, 2, True)
            if p.character == "jeff_alt":
                self.character_sprites["jeff_alt"] = {}
                self.character_sprites["jeff_alt"]["last_action"] = "forward"
                self.character_sprites["jeff_alt"]["profile"] = "SnakeEyes/Assets/Characters/Profile/Jeff Profile Alt1.png"
                self.character_sprites["jeff_alt"]["forward"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/Jeff-ForwardAlt1.png",
                                                                                         60, 75, 2)
                self.character_sprites["jeff_alt"]["back"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/JeffBackAlt1.png",
                                                                                      55, 75, 2)
                self.character_sprites["jeff_alt"]["right"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/JeffWalkRight Alt1.png",
                                                                                       65, 70, 2)
                self.character_sprites["jeff_alt"]["left"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/JeffWalkRight Alt1.png",
                                                                                      65, 70, 2, True)
            if p.character == "mj":
                self.character_sprites["mj"] = {}
                self.character_sprites["mj"]["last_action"] = "forward"
                self.character_sprites["mj"]["profile"] = "SnakeEyes/Assets/Characters/Profile/mj-profile.png"
                self.character_sprites["mj"]["forward"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MjForward.png",
                                                                                   60, 75, 2)
                self.character_sprites["mj"]["back"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MjBack.png",
                                                                                55, 75, 2)
                self.character_sprites["mj"]["right"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MJRightWalk.png",
                                                                                 65, 70, 2)
                self.character_sprites["mj"]["left"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MJRightWalk.png",
                                                                                65, 70, 2, True)
            if p.character == "mj_alt":
                self.character_sprites["mj_alt"] = {}
                self.character_sprites["mj_alt"]["last_action"] = "forward"
                self.character_sprites["mj_alt"]["profile"] = "SnakeEyes/Assets/Characters/Profile/mj-profileAlt.png"
                self.character_sprites["mj_alt"]["forward"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MjForwardAlt1.png",
                                                                                       60, 75, 2)
                self.character_sprites["mj_alt"]["back"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MjBackAlt.png",
                                                                                    55, 75, 2)
                self.character_sprites["mj_alt"]["right"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MjRightWalkAlt1.png",
                                                                                     65, 70, 2)
                self.character_sprites["mj_alt"]["left"] = self.makeCharacterSprite("SnakeEyes/Assets/Characters/Movement/MjRightWalkAlt1.png",
                                                                                    65, 70, 2, True)
    def controllerHandling(self):
        if self.pNum == 2:
            self.controllerAssignment(self.player, Preferences.BLUE_CONTROLS)

        if self.pNum == 3:
            self.controllerAssignment(self.player, Preferences.YELLOW_CONTROLS)

        if self.pNum == 4:
            self.controllerAssignment(self.player, Preferences.RED_CONTROLS)

    def clientInit(self, pNum, GC1, GC2):
        print("client init")
        self.GC1 = GC1
        self.GC2 = GC2
        self.pNum = pNum
        self.controllerHandling()
        
        while self.connected == False:
            #print("client")
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Trying to connect: "+GC1+".tcp.ngrok.io:"+GC2)
            self.c.connect((GC1+".tcp.ngrok.io",int(GC2)))
            check = self.c.recv(1024).decode()
            if check == "GameConnected":
                print(check)
                self.c.send("Hey Serv from GAME".encode())

                self.connected = True
                self.running = True
                self.assigned = True
        


    ### Initializes the game after updated the preferences ###
    def delayedInit(self):
        self.scene = 'mgame'
        
    ### Handles control assignment from game setup ###
    def controllerAssignment(self, player, controls):
        #print("assigning P"+str(player.playerNum)+": " +controls)
        if not pygame.joystick.get_init():
            pygame.joystick.init()

        if not hasattr(self, 'joystick_id'):
            self.joystick_id = 0  # Initialize joystick ID counter

        if controls == "Controller":
            # Assign joystick controller
            pygame.event.pump()
            joystick_count = pygame.joystick.get_count()

            if self.joystick_id < joystick_count:
                controller_type = "joystick"
                controller_ID = self.joystick_id
                controller_scheme = None  # Not needed for joystick
                self.joystick_id += 1
            else:
                # DEBUG STATEMENT
                # print(f"No joystick available for Player {player.playerNum}, defaulting to keyboard")

                controller_type = "keyboard"
                controller_ID = None

                # Default Controls
                if player.playerNum == 1:
                    controller_scheme = "WASD"
                elif player.playerNum == 2:
                    controller_scheme = "TFGH"
                elif player.playerNum == 3:
                    controller_scheme = "IJKL"
                elif player.playerNum == 4:
                    controller_scheme = "Arrows"
        elif controls == "None":
            controller_type = "None"
            controller_ID = None
            controller_scheme = controls
            
        else:
            # Assign keyboard controls
            controller_type = "keyboard"
            controller_ID = None
            controller_scheme = controls  # Ensuring this is a valid scheme
            

        # DEBUG STATEMENT
        # print(f"player {player.playerNum} assigned {controller_scheme}")
        # Create a Controller object and assign it to the player
        player.controller = controller.Controller(
            controller_type=controller_type,
            controller_ID=controller_ID,
            controller_scheme=controller_scheme
        )

        if player.controller.controller_type == "keyboard":
            player.left = player.controller.left
            player.right = player.controller.right
            player.up = player.controller.up
            player.down = player.controller.down

    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainGameLoop.mp3")

    ##### Run Game Loop #####
    def run(self):
        self.update() 
        if self.assigned:
            self.clientProcess()
        self.render()

    ##### Update Game #####
    def update(self):
        self.inputManagerCLIENT()
        
        #self.readyCheck()
        #self.colliderUpdate()

    def assignTunnel(self, pNum, c):
        self.pNum = pNum
        self.c = c

    def clientProcess(self):
        if self.running:
            try:
                #print("Running...")
                
        
                self.c.send(pickle.dumps(self.sendData()))
                game_state = pickle.loads(self.c.recv(4096))
                #print("Importing...")
                self.loadData(game_state)
                #self.dataImport()
                #
                #print("Updating...")
                #self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
                #self.update()
                #print("Rendering...")
                #self.render()
            except EOFError:
                print("Game End of Connection")
                print(self.tempScene)
                self.running = False
                if self.tempScene == 'mstatus':
                    #print("Controlls: "+Preferences.BLUE_CONTROLS)
                    self.scene_manager.scenes['mstatus'].clientInit(self.pNum, self.GC1, self.GC2)
                    self.closeConnection()
                    self.scene_manager.switch_scene('mstatus')
                elif  self.tempScene == 'mwin':
                    self.scene_manager.scenes['mwin'].clientInit(self.pNum, self.GC1, self.GC2)
                    self.closeConnection()
                    self.scene_manager.switch_scene('mwin')
                else:
                    self.scene_manager.switch_scene('menu')
                    self.scene_manager.multiplayer_destroy()

                self.c.close()
                print("GAME EoC Exiting...")

    def closeConnection(self):
        self.connected = False
        self.running = False
        self.assigned = False
        self.tempScene = 'mgame'

    ##### Render Game #####
    def render(self):
        self.characterMovement()

        ### Fill Background ###
        self.screen.fill((255,255,255))
        ### Set Background Image ###
        self.screen.blit(self.loadingScreen, (0,0))

        ### Render the Stores ###
        self.screen.blit(self.storeSprites[self.Stores[0].spriteNum], (140,50))
        self.screen.blit(self.storeSprites[self.Stores[1].spriteNum], (390,50))
        self.screen.blit(self.storeSprites[self.Stores[2].spriteNum], (640,50))
        self.screen.blit(self.storeSprites[self.Stores[3].spriteNum], (890,50))
        # Store info Panels
        self.screen.blit(self.storeInfoPanel, (148,6))
        self.screen.blit(self.storeInfoPanel, (398,6))
        self.screen.blit(self.storeInfoPanel, (648,6))
        self.screen.blit(self.storeInfoPanel, (898,6))

        ### All game status updates ###
        self.debugStatus()
        self.gameStatus()
        self.storeStatus()
        self.carStatus()
        self.playerStatus()

        if not self.statusFlag: #Prevents rendering the reset stuff when ending round
            pygame.display.flip()

    def loadData(self, game_state):
        #print("Load data")
        self.Players = game_state['Players']
        if len(self.Players) == 2:
            self.p1 = self.Players[0]
            self.p2 = self.Players[1]
        elif len(self.Players) == 3:
            self.p1 = self.Players[0]
            self.p2 = self.Players[1]
            self.p3 = self.Players[2]
        elif len(self.Players) == 4:
            self.p1 = self.Players[0]
            self.p2 = self.Players[1]
            self.p3 = self.Players[2]
            self.p4 = self.Players[3]

        #print("Players length: "+str(len(self.Players)))
        #print("Pnum: "+str(self.pNum))
        self.player = self.Players[self.pNum-1]
        self.controllerHandling()
        #print("Player position: "+str(self.player.position))
        self.lastRound = game_state['lastRound']
        self.statusFlag = game_state['statusFlag']
        self.result = game_state['result']
        self.police = game_state['police']
        self.ready = game_state['ready']
        self.alarmedStores = game_state['alarmedStores']
        self.allAlarms = game_state['allAlarms']
        self.Stores = game_state['Stores']
        #print("Store Length: " +str(len(self.Stores)))
        self.Cars = game_state['Cars']
        self.tempScene = game_state['Scene']

        if not self.charactersInitialized:
            self.charactersInitialized = True
            self.initializePlayerSprites()
        
        if not self.enabledControlls:
            self.enableControls()
            self.enabledControlls = True
        
        #if game_state['scene'] != self.scene:
        #    self.scene_manager.switch_scene(game_state['scene'])
            
    def enableControls(self):
        self.joystick_id = 0
        if Preferences.RED_PLAYER_TYPE == "Player" or Preferences.RED_PLAYER_TYPE == "CPU" or Preferences.RED_PLAYER_TYPE == "Player(Online)":
            self.controllerAssignment(self.Players[0], Preferences.RED_CONTROLS)

        if Preferences.BLUE_PLAYER_TYPE == "Player" or Preferences.BLUE_PLAYER_TYPE == "CPU" or Preferences.BLUE_PLAYER_TYPE == "Player(Online)":
            self.controllerAssignment(self.Players[1], Preferences.BLUE_CONTROLS)

        if Preferences.YELLOW_PLAYER_TYPE == "Player" or Preferences.YELLOW_PLAYER_TYPE == "CPU" or Preferences.YELLOW_PLAYER_TYPE == "Player(Online)":
            self.controllerAssignment(self.Players[2], Preferences.YELLOW_CONTROLS)

        if Preferences.GREEN_PLAYER_TYPE == "Player" or Preferences.GREEN_PLAYER_TYPE == "CPU" or Preferences.GREEN_PLAYER_TYPE == "Player(Online)":
            self.controllerAssignment(self.Players[3], Preferences.GREEN_CONTROLS)


    def debugStatus(self):
        ##### DEBUG / STATUS INFO #####
        if self.lastRound:
            self.GAME_FONT.render_to(self.screen, (350, 50), self.result, (0, 0, 0))

    ### On screen text for game status information ###
    def gameStatus(self):
        if self.police:
            self.GAME_FONT.render_to(self.screen, (350, 400), "Press SPACE to continue...", (255, 255, 255))
        else:
            if self.ready:
                self.GAME_FONT.render_to(self.screen, (350, 400), "Press SPACE to try your luck...", (255, 255, 255))
            else:
                self.GAME_FONT.render_to(self.screen, (350, 400), "Waiting for Players to Select a Store", (255, 255, 255))

        if self.alarmedStores > 0:
            if not self.police:
                if self.allAlarms:
                    self.GAME_FONT.render_to(self.screen, (350, 430), "All stores alarmed, time to leave the mall...", (255, 255, 255))
                else:
                    self.GAME_FONT.render_to(self.screen, (350, 430), "Police are on their way!", (255, 255, 255))
            else: 
                self.GAME_FONT.render_to(self.screen, (200, 430), "POLICE HAVE ARRIVED, ALL PLAYERS STILL IN LOSE THEIR SAVINGS", (255, 255, 255))

    ### Information associated with each store ###
    def storeStatus(self):
        for s in self.Stores:
            # Displays ALARMED and POLICE
            scoreTextRect = self.ALERT_FONT.get_rect(s.scoreText)
            scoreTextRect.center = (s.position.x+15, s.position.y-262)
            self.ALERT_FONT.render_to(self.screen, (scoreTextRect.left-1, scoreTextRect.top-1), s.scoreText, (255,255,255))
            self.ALERT_FONT.render_to(self.screen, (scoreTextRect.left, scoreTextRect.top), s.scoreText, s.scoreTextColor)

            if s.status == -1:
                s.color = (255,0,0)
            else:
                
                iconSize = 30
                iconOffset = 0
                
                # Risk
                scaledBadgeSprite = pygame.transform.scale(self.badgeSprite, (iconSize, iconSize))
                center_x, center_y = s.position.x+15, s.position.y-280 
                total_width = ((iconSize+iconOffset) * (s.risk)) - iconOffset 
                start_x = center_x - total_width // 2
                offset = 0
                for x in range(s.risk):
                    self.screen.blit(scaledBadgeSprite, (start_x+offset, center_y-(iconSize//2)))
                    offset += iconSize+iconOffset

                # Reward
                scaledMoneySprite = pygame.transform.scale(self.moneySprite, (iconSize, iconSize))
                center_x, center_y = s.position.x+15, s.position.y-245 
                total_width = ((iconSize+iconOffset) * (s.reward)) - iconOffset 
                start_x = center_x - total_width // 2
                offset = 0
                for x in range(s.reward):
                    self.screen.blit(scaledMoneySprite, (start_x+offset, center_y-(iconSize//2)))
                    offset += iconSize+iconOffset
                
                # Display players in the store
                # Lots of math because font size, text, and padding are all adjustable
                padding = 6
                back_color = (255, 255, 255)
                inactive_color = (65, 65, 65)
                showInactive = False # Enabling this shows all player numbers at all times in the inactive_color
                # PLAYER 1
                if hasattr(self, 'p1') and self.p1 in self.Players:
                    p_text = "P1"
                    p_text_rect = self.STORE_INFO_PANEL_FONT.get_rect(p_text)
                    p_text_rect.topleft = (s.position.x-99, s.position.y-300)

                    if self.p1 in s.players and self.p1.status == 1:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding-1, p_text_rect.top+padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding, p_text_rect.top+padding), p_text, self.p1.color)
                    elif showInactive:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding-1, p_text_rect.top+padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding, p_text_rect.top+padding), p_text, inactive_color)
                # PLAYER 2
                if hasattr(self, 'p2') and self.p2 in self.Players:
                    p_text = "P2"
                    p_text_rect = self.STORE_INFO_PANEL_FONT.get_rect(p_text)
                    p_text_rect.topright = (s.position.x+128, s.position.y-300)

                    if self.p2 in s.players and self.p2.status == 1:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding-1, p_text_rect.top+padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding, p_text_rect.top+padding), p_text, self.p2.color)
                    elif showInactive:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding-1, p_text_rect.top+padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding, p_text_rect.top+padding), p_text, inactive_color)
                # PLAYER 3
                if hasattr(self, 'p3') and self.p3 in self.Players:
                    p_text = "P3"
                    p_text_rect = self.STORE_INFO_PANEL_FONT.get_rect(p_text)
                    p_text_rect.bottomleft = (s.position.x-99, s.position.y-225)

                    if self.p3 in s.players and self.p3.status == 1:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding-1, p_text_rect.top-padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding, p_text_rect.top-padding), p_text, self.p3.color)
                    elif showInactive:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding-1, p_text_rect.top-padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left+padding, p_text_rect.top-padding), p_text, inactive_color)
                # PLAYER 4
                if hasattr(self, 'p4') and self.p4 in self.Players:
                    p_text = "P4"
                    p_text_rect = self.STORE_INFO_PANEL_FONT.get_rect(p_text)
                    p_text_rect.bottomright = (s.position.x+128, s.position.y-225)

                    if self.p4 in s.players and self.p4.status == 1:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding-1, p_text_rect.top-padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding, p_text_rect.top-padding), p_text, self.p4.color)
                    elif showInactive:
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding-1, p_text_rect.top-padding-1), p_text, back_color)
                        self.STORE_INFO_PANEL_FONT.render_to(self.screen, (p_text_rect.left-padding, p_text_rect.top-padding), p_text, inactive_color)

    ### Information associated with each player ###
    def playerStatus(self):
        ##### PLAYERS #####
        for p in self.Players:
            if p.status != -1:
                # Render sprite
                if p.status == 0:
                    for action_name, sprite in self.character_sprites[p.character].items():
                        # Check if this action is the last updated action for this character
                        if action_name == self.character_sprites[p.character]["last_action"]:
                            # Render the last updated sprite
                            adjusted_position = p.position - pygame.Vector2(30, 50)
                            self.screen.blit(sprite.current_sprite, adjusted_position)
        
            ### Constant player status information in the corners of the screen MOVE TO BOTTOM BANNER ###
            self.GAME_FONT.render_to(self.screen, (p.gr.x-18, p.gr.y-42), "$"+str(f'{round(p.score, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}'), (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-40), "$"+str(f'{round(p.score, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}'), (255, 255, 255))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-18, p.gr.y-22), "P"+str(p.playerNum), (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-20), "P"+str(p.playerNum), (255, 255, 255))

            self.GAME_FONT.render_to(self.screen, (p.gr.x-18, p.gr.y+8), "Mods" , (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y+10), "Mods" , Settings.COLOR_TEXT)
            offset = 0
            for m in p.currentMods:
                offset = offset + 20
                modImg = m.image
                modImg = pygame.transform.scale(m.image, (20,20))
                self.screen.blit(modImg, (p.gr.x-20, p.gr.y+8+offset))

            ### Player temp score information that is attached directly to the player ###
            if p.status == 0:
                printTemp = round(p.tmpScore+p.score, Settings.ROUNDING_PRECISION)
                self.GAME_FONT.render_to(self.screen, (p.position.x-21, p.position.y+19), "$"+str(f'{round(p.tmpScore, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}'), (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+20), "$"+str(f'{round(p.tmpScore, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}'), (255, 255, 255))
                self.GAME_FONT.render_to(self.screen, (p.position.x-21, p.position.y+39), "$"+str(f'{round(printTemp, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}'), (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+40), "$"+str(f'{round(printTemp, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}'), (175, 175, 175))
                self.GAME_FONT.render_to(self.screen, (p.position.x-16, p.position.y-69), "P"+str(p.playerNum), (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-15, p.position.y-70), "P"+str(p.playerNum), (255, 255, 255))
                self.GAME_FONT.render_to(self.screen, (p.position.x-21, p.position.y+59), p.scoreText, (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+60), p.scoreText, (0,255,0))


    ### Information and display of car ###
    def carStatus(self):
        for c in self.Cars:
            
            self.screen.blit(self.carSprites[c.carSpriteNum], c.position)
            for p in self.Players:
                if c.playerNum == p.playerNum:
                    if c.ready == True:
                        self.GAME_FONT.render_to(self.screen, (c.position.x+10, c.position.y-85), "P"+str(p.playerNum), (255,255,255))
                        self.GAME_FONT.render_to(self.screen, (c.position.x-60, c.position.y-60), "SELECT to Cash-Out", (255,255,255))

    # Updates character sprites
    def updateCharacterSprite(self, character_sprites, character, action):
        sprite = character_sprites[character][action]
        new_current_frame = sprite.current_frame + 1
        if new_current_frame >= len(sprite.sprite_list) * sprite.frame_rate:
            new_current_frame = 0
        new_current_sprite = sprite.sprite_list[new_current_frame // sprite.frame_rate]
        updated_state = sprite._replace(current_frame=new_current_frame, current_sprite=new_current_sprite)
        character_sprites[character][action] = updated_state #Save updated state
        character_sprites[character]["last_action"] = action

        
    def characterMovement(self):
        for p in self.Players:
            if p.mMoveY < 0:  # Moving up
                self.updateCharacterSprite(self.character_sprites, p.character, "back")
            elif p.mMoveY > 0:  # Moving down
                self.updateCharacterSprite(self.character_sprites, p.character, "forward")
            if p.mMoveX < 0:  # Moving left
                self.updateCharacterSprite(self.character_sprites, p.character, "left")
            elif p.mMoveX > 0:  # Moving right
                self.updateCharacterSprite(self.character_sprites, p.character, "right")

    
    def sendData(self):
        #print("Sending Data")
        game_state = {
                'moveX': self.move_x,
                'moveY': self.move_y,
                'readyKey': self.readyKey,
                'pauseKey': self.pauseKey,
                'msg': 'message',
                'Scene': self.tempScene
            }
        return game_state

    

    ### handles all inputs for the client ###
    def inputManagerCLIENT(self):
        #print("input: "+self.player.controller.controller_type)
        #dt = self.clock.tick(60) / 1000
        if self.player.controller.controller_type == "keyboard" or self.player.controller.controller_type == "joystick":
            self.move_x, self.move_y = self.player.controller.get_movement()
            #print("Input Tracking move_x "+str(self.move_x))
            for event in pygame.event.get():

                ### Handle application exit ###
                if event.type == pygame.QUIT:
                    self.running = False
                    self.c.shutdown(socket.SHUT_RDWR)
                    self.c.close()
                    self.scene_manager.quit()

                ### Handle keyboard events ###
                if event.type == pygame.KEYDOWN:
                    if event.key == self.player.controller.action_buttons.get('ready'):
                        self.readyKey = True
                        print("Player Status: "+str(self.player.status))
                    else:
                        self.readyKey = False

                    if event.key == pygame.K_ESCAPE:
                        self.pauseKey = True
                    else:
                        self.pauseKey = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    joystick_id = event.joy
                    button_id = event.button


                    if self.player.controller.controller_type == 'joystick':
                        if self.player.controller.joystick.get_instance_id() == joystick_id:
                            if button_id == self.player.controller.action_buttons.get('ready'):
                                self.readyKey = True
                            else:
                                self.readyKey = False

    def getScore(self, playerNum):
            for p in self.Players:
                if p.playerNum == playerNum:
                    return str(p.score)
    