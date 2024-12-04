import pygame
import pygame.locals
import pygame.freetype  # Import the freetype module.
import random
import math
from collections import namedtuple
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code import modifier
from SnakeEyes.Code import controller
from SnakeEyes.Code import player
from SnakeEyes.Code import car
from SnakeEyes.Code import store


### TO DO ###


### BUGS ###
# need to swap out space trigger for dice rolling, needs to work with controller and changed in test sim key
# store collision needs fixed
# dont set off police on first alarm
# last round hanling with police call/all alarms going straight to win screen


### FEATURE CHANGES ###
# attach vault score to vehicle


########## GAME ##########
class Game:
    ##### Initial Setup #####
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.STORE_INFO_PANEL_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 18)
        self.ALERT_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 30)
        self.clock = pygame.time.Clock()
        self.initialization()


    def initialization(self):
        ### Flags and General Game Vars ###
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
        self.storeCollider = pygame.Rect((0, 0, 1280, 260)) 

        self.loadingScreen = pygame.image.load('SnakeEyes/Assets/Environment/Background/Background.png')
        self.badgeSprite = pygame.image.load('SnakeEyes/Assets/Icons/badge.png')
        self.moneySprite = pygame.image.load('SnakeEyes/Assets/Icons/cash.png')
        self.storeInfoPanel = pygame.image.load('SnakeEyes/Assets/Environment/Background/Store_Info_Panel.png')
        self.storeSprites = [
            "SnakeEyes/Assets/Environment/Objects/ABC_Liquor.png",
            "SnakeEyes/Assets/Environment/Objects/Perris_Jewels.png",
            "SnakeEyes/Assets/Environment/Objects/RX-Express.png",
            "SnakeEyes/Assets/Environment/Objects/Slow_Panda.png"
        ]
        self.playerReset()
        self.playerLocReset()
        self.storeReset()

        self.initializePlayerSprites()

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
        self.character_sprites = {}

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

    ### Initializes the game after updated the preferences ###
    def delayedInit(self):
        self.winScore = Preferences.FINISHLINE_SCORE
        self.playerReset()
        self.playerLocReset()
        self.storeReset()
        self.CarReset()

    ### Resets all stores to starting state ###
    def storeReset(self):

        # Pick new store sprites
        selected_sprites = random.sample(self.storeSprites, 4)

        self.store1 = store.Store()
        self.store1.storeNum = 1
        self.store1.position = pygame.Vector2(250, 310)
        self.assignStoreStats(self.store1)
        self.store1.sprite = pygame.image.load(selected_sprites[0])

        self.store2 = store.Store()
        self.store2.storeNum = 2
        self.store2.position = pygame.Vector2(500, 310)
        self.assignStoreStats(self.store2)
        self.store2.sprite = pygame.image.load(selected_sprites[1])

        self.store3 = store.Store()
        self.store3.storeNum = 3
        self.store3.position = pygame.Vector2(750, 310)
        self.assignStoreStats(self.store3)
        self.store3.sprite = pygame.image.load(selected_sprites[2])

        self.store4 = store.Store()
        self.store4.storeNum = 4
        self.store4.position = pygame.Vector2(1000, 310)
        self.assignStoreStats(self.store4)
        self.store4.sprite = pygame.image.load(selected_sprites[3])

        self.Stores = [self.store1,self.store2,self.store3, self.store4]

        for s in self.Stores:
            s.collider = pygame.Rect(s.position.x-33, s.position.y, 100,20)

    ### Resets all Players to starting state ###
    def playerReset(self):
        self.Players = []
        self.joystick_id = 0
        if Preferences.RED_PLAYER_TYPE == "Player" or Preferences.RED_PLAYER_TYPE == "CPU":
            self.p1 = player.Player()
            self.p1.playerNum = 1
            self.controllerAssignment(self.p1, Preferences.RED_CONTROLS)
            self.p1.color = (255,0,0)
            self.p1.character = Preferences.RED_CHARACTER
            self.p1.gr = pygame.Vector2(25,60)
            self.p1.yl = pygame.Vector2(25,80)
            self.p1.rd = pygame.Vector2(25,100)
            self.Players.append(self.p1)

        if Preferences.BLUE_PLAYER_TYPE == "Player" or Preferences.BLUE_PLAYER_TYPE == "CPU":
            self.p2 = player.Player()
            self.p2.playerNum = 2
            self.controllerAssignment(self.p2, Preferences.BLUE_CONTROLS)
            self.p2.color = (0,0,255)
            self.p2.character = Preferences.BLUE_CHARACTER
            self.p2.gr = pygame.Vector2(1210,60)
            self.p2.yl = pygame.Vector2(1210,80)
            self.p2.rd = pygame.Vector2(1210,100)
            self.Players.append(self.p2)

        if Preferences.YELLOW_PLAYER_TYPE == "Player" or Preferences.YELLOW_PLAYER_TYPE == "CPU":
            self.p3 = player.Player()
            self.p3.playerNum = 3
            self.controllerAssignment(self.p3, Preferences.YELLOW_CONTROLS)
            self.p3.color = (204,204,0)
            self.p3.character = Preferences.YELLOW_CHARACTER
            self.p3.gr = pygame.Vector2(25,260)
            self.p3.yl = pygame.Vector2(25,280)
            self.p3.rd = pygame.Vector2(25,300)
            self.Players.append(self.p3)

        if Preferences.GREEN_PLAYER_TYPE == "Player" or Preferences.GREEN_PLAYER_TYPE == "CPU" :
            self.p4 = player.Player()
            self.p4.playerNum = 4
            self.controllerAssignment(self.p4, Preferences.GREEN_CONTROLS)
            self.p4.color = (0,255,0)
            self.p4.character = Preferences.GREEN_CHARACTER
            self.p4.gr = pygame.Vector2(1210,260)
            self.p4.yl = pygame.Vector2(1210,280)
            self.p4.rd = pygame.Vector2(1210,300)
            self.Players.append(self.p4)

        self.numPlayers = len(self.Players)

    ### Resets all Cars to starting state ###
    def CarReset(self):
        self.Cars = []

        if Preferences.RED_PLAYER_TYPE != "None":
            self.c1 = car.Car()
            self.c1.playerNum = self.p1.playerNum
            self.c1.position = pygame.Vector2(110, 520)
            self.c1.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP1.png')
            self.c1.carSprite = pygame.transform.scale(self.c1.carSprite, (60,150))
            self.Cars.append(self.c1)
        

        if Preferences.BLUE_PLAYER_TYPE != "None":
            self.c2 = car.Car()
            self.c2.playerNum = self.p2.playerNum
            self.c2.position = pygame.Vector2(310, 520)
            self.c2.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP2.png')
            self.c2.carSprite = pygame.transform.scale(self.c2.carSprite, (60,150))
            self.Cars.append(self.c2)

        if Preferences.YELLOW_PLAYER_TYPE != "None":
            self.c3 = car.Car()
            self.c3.playerNum = self.p3.playerNum
            self.c3.position = pygame.Vector2(715, 520)
            self.c3.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP3.png')
            self.c3.carSprite = pygame.transform.scale(self.c3.carSprite, (60,150))
            self.Cars.append(self.c3)

        if Preferences.GREEN_PLAYER_TYPE != "None":
            self.c4 = car.Car()
            self.c4.playerNum = self.p4.playerNum
            self.c4.position = pygame.Vector2(1020, 520)
            self.c4.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP4.png')
            self.c4.carSprite = pygame.transform.scale(self.c4.carSprite, (60,150))
            self.Cars.append(self.c4)

        for c in self.Cars:
            c.collider = pygame.Rect(c.position.x-20, c.position.y-20, 100,190)
            c.rb = pygame.Rect(c.position.x, c.position.y, 60,150)

    ### Resets all Player Statuses ###
    def playerStatusReset(self):
        for p in self.Players:
            p.status = 0
            p.scoreText = ""

    ### Resets player location to starting point ###
    def playerLocReset(self):
        if Preferences.RED_PLAYER_TYPE != "None":
            self.p1.position = pygame.Vector2(140,470)
        if Preferences.BLUE_PLAYER_TYPE != "None":
            self.p2.position = pygame.Vector2(340,470)
        if Preferences.YELLOW_PLAYER_TYPE != "None":
            self.p3.position = pygame.Vector2(750,470)
        if Preferences.GREEN_PLAYER_TYPE != "None":
            self.p4.position = pygame.Vector2(1040,470)

    ### Handles control assignment from game setup ###
    def controllerAssignment(self, player, controls):
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
        self.render()

    ##### Update Game #####
    def update(self):
        self.inputManager()
        self.readyCheck()
        self.colliderUpdate()

    ##### Render Game #####
    def render(self):
        ### Fill Background ###
        self.screen.fill((255,255,255))
        ### Set Background Image ###
        self.screen.blit(self.loadingScreen, (0,0))
        
        ### Render the Stores ###
        self.screen.blit(self.store1.sprite, (140,50))
        self.screen.blit(self.store2.sprite, (390,50))
        self.screen.blit(self.store3.sprite, (640,50))
        self.screen.blit(self.store4.sprite, (890,50))
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
                self.GAME_FONT.render_to(self.screen, (p.position.x-14, p.position.y-68), "P"+str(p.playerNum), (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-16, p.position.y-70), "P"+str(p.playerNum), (255, 255, 255))
                self.GAME_FONT.render_to(self.screen, (p.position.x-15, p.position.y-69), "P"+str(p.playerNum), (p.color))
                self.GAME_FONT.render_to(self.screen, (p.position.x-21, p.position.y+59), p.scoreText, (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+60), p.scoreText, (0,255,0))


    ### Information and display of car ###
    def carStatus(self):
        for c in self.Cars:
            
            self.screen.blit(c.carSprite, c.position)
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

    ### Handles all collider checks ###
    def colliderUpdate(self):
        self.storeColliders()
        self.carColliders()

    ##### STORE COLLIDERS #####
    ### checks for any players colliding with the store col, adds them to the store if they're not in yet
    def storeColliders(self):
        for s in self.Stores:
            for p in self.Players:
                if p.status != -1:
                    collide = s.collider.colliderect(p.collider)
                    if s.status != -1:
                        if collide:
                            if p not in s.players:
                                s.players.append(p)
                        else:
                            if len(s.players) == 0:
                                s.color = (0, 0, 255)
                            if p in s.players:
                                s.players.remove(p)
                                p.status = 0
    
    ##### CAR COLLIDERS #####
    ### check for specified player's colision, sets option for cash out if collision is true
    def carColliders(self):
        for c in self.Cars:
            for p in self.Players:
                if c.playerNum == p.playerNum:
                    collide = c.collider.colliderect(p.collider)
                    if collide and p.status != -1:
                        c.ready = True
                    else:
                        c.ready = False

    # temp X & Y are where the player is intending on going, loc x & Y are where the player actually is
    def boundaryCollision(self, player, tempX, tempY, locX, locY):
        valid = False
        # exterior boarder
        if(tempX != 0):
            if (locX < 1260 or tempX < 0) and (locX> 20 or tempX > 0):
                valid = True
            else:
                # print("Border Hit")
                return False

        if(tempY != 0):
            if (locY < 700 or tempY < 0) and (locY > 20 or tempY > 0):
                valid = True
            else:
                # print("Border Hit")
                return False

        # premptive collision check
        if(tempX != 0):
            player.XCol.center = pygame.Vector2(player.position.x+tempX/11, player.position.y)
            # print("New Location X: "+str(tempCol.center))
        if(tempY != 0):
            player.YCol.center = pygame.Vector2(player.position.x, player.position.y+tempY/11)
            # print("New Location Y: "+str(tempCol.center))

        collideX = self.storeCollider.colliderect(player.XCol)
        collideY = self.storeCollider.colliderect(player.YCol)

        if collideX or collideY:
            valid = False

        for c in self.Cars:
            collideX = c.rb.colliderect(player.XCol)
            collideY = c.rb.colliderect(player.YCol)

            if collideX or collideY:
                valid = False

        player.XCol.center = player.position
        player.YCol.center = player.position

        return valid


    ### checks ready status for all players
    def readyCheck(self):
        count = 0
        for p in self.Players:
            if p.status == 0:
                count = count + 1

        if count != 0:
            self.ready = False
        else:
            self.ready = True

    ##### Game Functions #####

    ### handles all inputs for the game ###
    def inputManager(self):
        if self.statusFlag:
            self.resetRound()

        dt = self.clock.tick(60) / 1000

        ##### Player Controls #####

        if not self.police:
            for p in self.Players:
                if p.controller.controller_type == "keyboard" or p.controller.controller_type == "joystick":
                    #Handles Players
                    if p.status != -1:
                        if self.scene_manager.current_scene == "game":
                            # Update player status if moving
                            
                            if p.controller.get_movement() != (0, 0) and p.status == 1:

                            #print("Reset")
                                p.status = 0

                        move_x, move_y = p.controller.get_movement()
                        tempX = move_x * self.moveSpeed
                        tempY = move_y * self.moveSpeed
                            
                        # Update character sprite based on movement direction
                        if move_y < 0:  # Moving up
                            self.updateCharacterSprite(self.character_sprites, p.character, "back")
                        elif move_y > 0:  # Moving down
                            self.updateCharacterSprite(self.character_sprites, p.character, "forward")
                        if move_x < 0:  # Moving left
                            self.updateCharacterSprite(self.character_sprites, p.character, "left")
                        elif move_x > 0:  # Moving right
                            self.updateCharacterSprite(self.character_sprites, p.character, "right")

                        
                        if tempX != 0 or tempY != 0:
                            # if both, check for both
                            if tempX != 0 and tempY != 0:
                                #print("both")
                                if self.boundaryCollision(p, tempX, 0,p.position.x, p.position.y):
                                    tempX = tempX*(math.sqrt(2)/2)
                                else:
                                    tempX = 0
                                
                                if self.boundaryCollision(p, 0, tempY, p.position.x, p.position.y):
                                    tempY = tempY*(math.sqrt(2)/2)
                                else:
                                    tempY = 0
                                #print("vars: "+tempX+" "+tempY)
                                
                            # if h check      
                            elif tempX != 0 and tempY == 0:
                                #print("X")
                                if not self.boundaryCollision(p, tempX, 0,p.position.x, p.position.y):
                                    tempX = 0
                            # if y check 
                            elif tempX == 0 and tempY != 0:
                                #print("Y")
                                if not self.boundaryCollision(p, 0, tempY, p.position.x, p.position.y):
                                    tempY = 0 

                            p.position.x += tempX * dt
                            p.position.y += tempY * dt
                            p.collider.center = p.position
                else:
                    #print("CPU")
                    #handles CPU
                    self.CPUDumbManager(p, dt)

        for event in pygame.event.get():

            ### Handle application exit ###
            if event.type == pygame.QUIT:
                self.scene_manager.quit()
                self.running = False

            ### Handle keyboard events ###
            if event.type == pygame.KEYDOWN:

                #### Used for Keyboard Emulation Testing // Player controls pt. 2 ####
                if self.testing and self.scene_manager.current_scene == "game":

                    if not self.police:
                        for p in self.Players:
                            if p.status != -1:
                                tempX = 0
                                tempY = 0
                                if event.key == p.up:
                                    tempY -= self.moveSpeed
                                if event.key == p.down:
                                    tempY += self.moveSpeed
                                if event.key == p.left:
                                    tempX -= self.moveSpeed
                                if event.key == p.right:
                                    tempX += self.moveSpeed

                                # if p.position.x + tempX < 1510 and p.position.x + tempX > -250 and p.position.y + tempY < 950 and p.position.y + tempY > -250:
                                if tempX != 0 or tempY != 0:
                                    # if both, check for both
                                    if tempX != 0 and tempY != 0:
                                        # print("both")
                                        if self.boundaryCollision(
                                            p, tempX, 0, p.position.x, p.position.y
                                        ):
                                            tempX = tempX * (math.sqrt(2) / 2)
                                        else:
                                            tempX = 0

                                        if self.boundaryCollision(
                                            p, 0, tempY, p.position.x, p.position.y
                                        ):
                                            tempY = tempY * (math.sqrt(2) / 2)
                                        else:
                                            tempY = 0

                                    elif tempX != 0 and tempY == 0:
                                        # print("X")
                                        if not self.boundaryCollision(
                                            p, tempX, 0, p.position.x, p.position.y
                                        ):
                                            tempX = 0
                                    # if y check
                                    elif tempX == 0 and tempY != 0:
                                        # print("Y")
                                        if not self.boundaryCollision(
                                            p, 0, tempY, p.position.x, p.position.y
                                        ):
                                            tempY = 0

                                    p.position.x += tempX * dt
                                    p.position.y += tempY * dt
                                    p.collider.center = p.position

                for p in self.Players:
                    if p.controller.controller_type == 'keyboard':
                        if event.key == p.controller.action_buttons.get('space'):
                            if p.playerNum == 1:
                                # DEBUG STATEMENT
                                #print("space pressed...")
                                self.handle_dice_roll()

                        elif event.key == p.controller.action_buttons.get('ready'):
                            # DEBUG STATEMENT
                            # print("ready pressed...")
                            self.handle_ready_action(p)


                if event.key == pygame.K_ESCAPE:
                    if not self.testing:
                        self.scene_manager.switch_scene("pause")

            ### joystick events ###
            elif event.type == pygame.JOYBUTTONDOWN:
                joystick_id = event.joy
                button_id = event.button

                for p in self.Players:
                    if p.controller.controller_type == 'joystick':
                        if p.controller.joystick.get_instance_id() == joystick_id:
                            if button_id == p.controller.action_buttons.get('space'):
                                # DEBUG STATEMENT
                                # print("space pressed...")
                                self.handle_dice_roll()
                            elif button_id == p.controller.action_buttons.get('ready'):
                                # DEBUG STATEMENT
                                # print("ready pressed...")
                                self.handle_ready_action(p)

    ### CPU SECTION ###
    # if cpu has nowhere to go, find somewhere to go
    def CPUDumbManager(self, p, dt):
        if p.controller.controller_type == "None":
            if p.status != -1:
                if self.scene_manager.current_scene == "game":
                    # Update player status if moving
                    if p.CPU.moveToLocation == (0,0):
                        p.CPU.moveToLocation = self.CPUSelectLocation(p)
                    else:
                        self.CPUMoveToLocation(p, dt)
                        #move to location

    ### Figures out which location to go to
    def CPUSelectLocation(self, CPU):
        #selecting store
        if self.CPUDecidePlay(CPU) == True:
            activeStores = []
            for s in self.Stores:
                if s.status == 0:
                    activeStores.append(s)
            position = activeStores[random.randint(0, len(activeStores)-1)].position
            modPos = pygame.Vector2(position.x+30, position.y)
            return modPos
        else:
            #selecting Car
            for c in self.Cars:
                ##### if at car cash out
                if c.playerNum == CPU.playerNum:
                    #print(c.position)
                    return c.position
                    # position = pygame.Vector2(c.position.x + 30, c.position.y)
                    # print(c.position)
                    # return position

    def CPUHighThreshold(self):
        highestScore = max(p.score for p in self.Players)
        return highestScore

    def CPULowThreshold(self):
        lowestScore = min(p.score for p in self.Players)
        return lowestScore   
            
    def CPUDecidePlay(self, CPU):
        if any(store.status == -1 for store in self.Stores):
            if random.random() < 0.5:
                car=random.choice(self.Cars)
                CPU.CPU.moveToLocation = pygame.Vector2(car.position.x, car.position.y)
                return False
            else:
                return True

        if CPU.CPU.turn < 5:
            return True
        return False
    
    ### CPU Movement ###
    def CPUMoveToLocation(self, CPU, dt):
        
        #cpu counter delays the cpu from moving instantly
        if CPU.CPU.counter < 90 and CPU.status == 0:
            #print("Waiting...")
            CPU.CPU.counter += 1
        elif CPU.status == 0:            
            
            if CPU.CPU.moveToLocation.x < CPU.position.x+7 and CPU.CPU.moveToLocation.x > CPU.position.x-7:
                move_x = 0
            elif CPU.CPU.moveToLocation.x > CPU.position.x:
                move_x = 1
            elif CPU.CPU.moveToLocation.x < CPU.position.x:
                move_x = -1
            else:
                move_x = 0

            if CPU.CPU.moveToLocation.y < CPU.position.y+7 and CPU.CPU.moveToLocation.y > CPU.position.y-7:
                move_y = 0
            elif CPU.CPU.moveToLocation.y > CPU.position.y:
                move_y = 1
            elif CPU.CPU.moveToLocation.y < CPU.position.y:
                move_y = -1
            else:
                move_y = 0

            tempX = move_x * self.moveSpeed
            tempY = move_y * self.moveSpeed
                
            # Update character sprite based on movement direction
            if move_y < 0:  # Moving up
                self.updateCharacterSprite(self.character_sprites, CPU.character, "back")
            elif move_y > 0:  # Moving down
                self.updateCharacterSprite(self.character_sprites, CPU.character, "forward")
            if move_x < 0:  # Moving left
                self.updateCharacterSprite(self.character_sprites, CPU.character, "left")
            elif move_x > 0:  # Moving right
                self.updateCharacterSprite(self.character_sprites, CPU.character, "right")

            
            if tempX != 0 or tempY != 0:
                # if both, check for both
                if tempX != 0 and tempY != 0:
                    #print("both")
                    if self.boundaryCollision(CPU, tempX, 0,CPU.position.x, CPU.position.y):
                        tempX = tempX*(math.sqrt(2)/2)
                    else:
                        tempX = 0
                    
                    if self.boundaryCollision(CPU, 0, tempY, CPU.position.x, CPU.position.y):
                        tempY = tempY*(math.sqrt(2)/2)
                    else:
                        tempY = 0
                    #print("vars: "+tempX+" "+tempY)
                    

                elif tempX != 0 and tempY == 0:
                    #print("X")
                    if not self.boundaryCollision(CPU, tempX, 0,CPU.position.x, CPU.position.y):
                        tempX = 0
                elif tempX == 0 and tempY != 0:
                    #print("Y")
                    if not self.boundaryCollision(CPU, 0, tempY, CPU.position.x, CPU.position.y):
                        tempY = 0 

                CPU.position.x += tempX * dt
                CPU.position.y += tempY * dt
                CPU.collider.center = CPU.position

                if abs(CPU.CPU.moveToLocation.x - CPU.position.x) < 100 and abs(CPU.CPU.moveToLocation.y - CPU.position.y) < 100 and CPU.status == 0:
                    if self.handle_ready_action(CPU):
                        CPU.CPU.counter = 0
    
    ### Handles when player or CPU readies ###
    def handle_ready_action(self, player):
        for c in self.Cars:
            ##### if at car cash out
            if c.ready and c.playerNum == player.playerNum:
                player.score = player.score + player.tmpScore
                player.tmpScore = 0
                player.status = -1
                self.Cars.remove(c)
                self.roundCheck()
                return True
            else:
            #### if at store, set to ready
                for s in self.Stores:
                    if player in s.players:
                        if player.status != -1:
                            player.status = 1
                            return True

    ### HANDLES THE DICE ROLL - SHOCKER ###
    def handle_dice_roll(self):
        # DEBUG STATEMENT
        # Clear store text
        for s in self.Stores:
            if s.scoreText != "ALARMED" and s.scoreText != "POLICE":
                s.scoreText = ''
                s.scoreTextColor = (255,255,255)

        self.roundCheck()

        
        ### handles if police have been triggered
        if self.police:
            if self.lastRound:
                self.gameOver()
            else:
                self.resetRound()
        ### handles if all alarms were set off
        elif self.allAlarms:
            if self.lastRound:
                self.gameOver()
            else:
                self.resetRound()
        else: 
            if self.ready:
                for s in self.Stores:
                    if len(s.players) != 0:
                        #police roll if a store is alarmed
                        if self.alarmedStores > 0 and self.roundSkipped:
                            if self.roll(1,(len(self.Stores)+11-self.alarmedStores),1,1) == -1:
                                self.policeRoll(s)

                        if not self.police:
                            # roll for value/alarm
                            self.award = self.roll(1,9,s.risk,s.reward) 

                            if self.award == -1:
                                self.alarmedStoreRoll(s)
                            else:
                                #print("Default Roll Started")
                                self.defaultRoll(s)
        # check for all alarms
        count = 0
        for s in self.Stores:
            if s.status == -1:
                count = count + 1

        self.alarmedStores = count

        if count == len(self.Stores):
            self.allAlarms = True


        # delays police roll from happening until the first alarmed round has finished
        if self.alarmedStores > 0 and not self.roundSkipped:
            self.roundSkipped = True

    
    ### Executes the police roll ###
    def policeRoll(self, store):
        #print("Police Roll")
        self.resetTempScores()
        store.scoreText = "POLICE"
        store.scoreTextColor = (0,0,255)
        store.status = -1
        self.police = True

        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/policeSiren.mp3")

        for p in self.Players:
            
            if p.status != -1:
                if modifier.paid_off not in p.currentMods:
                    p.score = 0
                else:
                    del p.currentMods[modifier.paid_off]
                p.status = -1
                if modifier.lucky_streak in p.currentMods:
                    del p.currentMods[modifier.lucky_streak]
                    p.streak = 0
        if not self.lastRound:
            self.result = "SNAKE EYES"

    ### Executes the alarm roll ###
    def alarmedStoreRoll(self, store):
        store.scoreText = "ALARMED"
        store.scoreTextColor = (255,0,0)
        self.alarmedStores = self.alarmedStores + 1
        store.status=-1

        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/alarm.mp3")

        for p in store.players:
            p.status = 0
            p.scoreText = ""
            p.streak = 0
            if modifier.On_a_roll not in p.currentMods:
                p.tmpScore = 0
            else:
                del p.currentMods[modifier.On_a_roll]

            if modifier.lucky_streak in p.currentMods:
                del p.currentMods[modifier.lucky_streak]
                p.streak = 0

            if p.controller.controller_type != "keyboard" and p.controller.controller_type != "joystick":
                p.CPU.turn += 1
                p.CPU.moveToLocation = (0,0)

                    

        store.players.clear()
    
    ### Executes Roll ###
    def defaultRoll(self, store):
        self.result = "Roll Default"
        for p in store.players:
            if p.status == 1:
                printScore = 0
                
                if modifier.lucky_streak in p.currentMods:
                    p.streak = p.streak + 1
                    printScore = modifier.lucky_streak_modifier(self.award, p.streak)
                    p.tmpScore = p.tmpScore+printScore
                else:
                    printScore = self.award
                    p.tmpScore = p.tmpScore+printScore
                
                p.tmpScore = round(p.tmpScore, Settings.ROUNDING_PRECISION)
                printScore = round(printScore, Settings.ROUNDING_PRECISION)
                p.status = 0
                p.scoreText = "+"+str(f'{round(printScore, Settings.ROUNDING_PRECISION):,.{Settings.ROUNDING_PRECISION}f}')
                store.scoreTextColor = (0,255,0)

            if p.controller.controller_type != "keyboard" and p.controller.controller_type != "joystick":
                p.CPU.turn += 1
                p.CPU.moveToLocation = (0,0)

    

    ### handles rolls, num 1 is the lowest number, num2 is highest number, risk is the level of risk mod applied, reward is the level of reward mod applied
    def roll(self, num1, num2, riskMod, rewardMod):
        self.roll1 = random.randint(num1, num2-(riskMod-1))
        self.roll2 = random.randint(num1, num2-(riskMod-1))
        if self.roll1 == self.roll2:
            return -1
        else: 
            return int((self.roll1+self.roll2)*self.rewardScale(rewardMod)*2000)

    ### handles the reward scaling
    def rewardScale(self, rewardMod):
        match rewardMod:
            case 1:
                return 0.5
            case 2:
                return 1.0
            case 3:
                return 1.25
            case 4:
                return 3.0
            case 5:
                return 5.0

    ### Assigns store stats ###
    def assignStoreStats(self, store):
        store.status = 0

        store.risk = random.randint(1,5)
        store.reward = (store.risk + random.randint(1,4) - 2)

        if store.reward < 1:
            store.reward = 1
        elif store.reward > 5:
            store.reward = 5

    ### looks through players to see if the round is over and how to handle it ###
    def roundCheck(self):
        self.lastRoundCheck()

        count = 0
        for p in self.Players:
            if p.status == -1:
                count = count + 1

        if count == self.numPlayers:
            if not self.lastRound:
                for p in self.Players:
                    p.status = 0
                    p.tmpScore = 0
                    count = 0
                    self.alarmedStores = 0
                    self.storeReset()
                    self.playerLocReset()
                    self.CarReset()
            else:
                count = 0
                self.gameOver()
            self.statusFlag = True

    def resetTempScores(self):
        for p in self.Players:
            p.tmpScore = 0

    ### Resets all of the cpu variables ###
    def resetCPU(self):
        for p in self.Players:
            if p.controller.controller_type != "keyboard" and p.controller.controller_type != "joystick":
                p.CPU.turn = 0
                p.CPU.moveToLocation = (0,0)
                ###reset threshold

    ### get's num of active players
    def lastRoundCheck(self):
        if not self.lastRound:
            for p in self.Players:
                if p.score >= self.winScore:
                    if self.getActivePlayers() > 0:
                        self.lastRound = True
                        self.result = "LAST ROUND"
                    else:
                        self.gameOver()

    ### Executes the end of game functions ###
    def gameOver(self):
        if not self.gameOverFlag:
            self.gameOverFlag = True
            self.TopPlayer = player.Player()
            self.HighScore = 0
            for p in self.Players:
                if p.score > self.HighScore:
                    self.TopPlayer = p
                    self.HighScore = p.score

            self.result = "GAME OVER: Player " + str(self.TopPlayer.playerNum) +" Wins!\nPress Space To Restart"
            self.scene_manager.switch_scene('win')

    ### Executres end of round functions ###
    def resetRound(self):
        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        if not self.lastRound:
            self.result = "RoundReset"
        self.allAlarms = False
        self.police = False
        self.alarmedStores = 0
        self.playerStatusReset()
        self.resetTempScores()
        self.playerLocReset()
        self.storeReset()
        self.CarReset()
        self.resetCPU()
        self.roundSkipped = False
        self.scene_manager.switch_scene('status')
        # print("Scene2")

    ### Executes game reset funcitons ###   
    def resetGame(self):
        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        self.result = "GameReset"
        self.lastRound = False
        self.allAlarms = False
        self.police = False
        self.alarmedStores = 0
        self.playerReset()
        self.playerLocReset()
        self.storeReset()
        self.CarReset()
        self.resetCPU()
        self.gameOverFlag = False
        self.statusFlag = True
        self.roundSkipped = False

    def getScore(self, playerNum):
            for p in self.Players:
                if p.playerNum == playerNum:
                    return str(p.score)
    
    def getActivePlayers(self):
        count = 0
        for p in self.Players:
            if p.status != -1:
                count = count +1
        return count
    
    