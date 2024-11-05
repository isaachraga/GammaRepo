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

        self.clock = pygame.time.Clock()

        self.initialization()

        # self.tests = Tests() #automated testing
        # self.tests.run_tests(self)

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
        self.storeCollider = pygame.Rect((140, 0, 990, 260)) 

        self.loadingScreen = pygame.image.load('SnakeEyes/Assets/Environment/Background/Background.png')
        self.badgeSprite = pygame.image.load('SnakeEyes/Assets/Icons/badge.png')
        self.moneySprite = pygame.image.load('SnakeEyes/Assets/Icons/cash.png')
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
        self.store1 = store.Store()
        self.store1.storeNum = 1
        self.store1.position = pygame.Vector2(250, 310)
        self.assignStoreStats(self.store1)

        self.store2 = store.Store()
        self.store2.storeNum = 2
        self.store2.position = pygame.Vector2(500, 310)
        self.assignStoreStats(self.store2)

        self.store3 = store.Store()
        self.store3.storeNum = 3
        self.store3.position = pygame.Vector2(750, 310)
        self.assignStoreStats(self.store3)

        self.store4 = store.Store()
        self.store4.storeNum = 4
        self.store4.position = pygame.Vector2(1000, 310)
        self.assignStoreStats(self.store4)

        self.Stores = [self.store1,self.store2,self.store3, self.store4]

        for s in self.Stores:
            s.collider = pygame.Rect(s.position.x, s.position.y, 20,20)

    def playerReset(self):
        self.Players = []
        self.joystick_id = 0
        if Preferences.RED_PLAYER_TYPE == "Player":
            self.p1 = player.Player()
            self.p1.playerNum = 1
            self.controllerAssignment(self.p1, Preferences.RED_CONTROLS)
            self.p1.color = (255,0,0)
            self.p1.character = Preferences.RED_CHARACTER
            self.p1.gr = pygame.Vector2(25,60)
            self.p1.yl = pygame.Vector2(25,80)
            self.p1.rd = pygame.Vector2(25,100)
            self.Players.append(self.p1)

        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.p2 = player.Player()
            self.p2.playerNum = 2
            self.controllerAssignment(self.p2, Preferences.BLUE_CONTROLS)
            self.p2.color = (0,0,255)
            self.p2.character = Preferences.BLUE_CHARACTER
            self.p2.gr = pygame.Vector2(1210,60)
            self.p2.yl = pygame.Vector2(1210,80)
            self.p2.rd = pygame.Vector2(1210,100)
            self.Players.append(self.p2)

        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.p3 = player.Player()
            self.p3.playerNum = 3
            self.controllerAssignment(self.p3, Preferences.YELLOW_CONTROLS)
            self.p3.color = (204,204,0)
            self.p3.character = Preferences.YELLOW_CHARACTER
            self.p3.gr = pygame.Vector2(25,260)
            self.p3.yl = pygame.Vector2(25,280)
            self.p3.rd = pygame.Vector2(25,300)
            self.Players.append(self.p3)

        if Preferences.GREEN_PLAYER_TYPE == "Player":
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

    ### Resets all carts to starting state ###
    def CarReset(self):
        self.Cars = []

        if Preferences.RED_PLAYER_TYPE == "Player":
            self.c1 = car.Car()
            self.c1.playerNum = self.p1.playerNum
            self.c1.position = pygame.Vector2(110, 520)
            self.c1.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP1.png')
            self.Cars.append(self.c1)

        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.c2 = car.Car()
            self.c2.playerNum = self.p2.playerNum
            self.c2.position = pygame.Vector2(310, 520)
            self.c2.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP2.png')
            self.Cars.append(self.c2)

        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.c3 = car.Car()
            self.c3.playerNum = self.p3.playerNum
            self.c3.position = pygame.Vector2(715, 520)
            self.c3.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP3.png')
            self.Cars.append(self.c3)

        if Preferences.GREEN_PLAYER_TYPE == "Player":
            self.c4 = car.Car()
            self.c4.playerNum = self.p4.playerNum
            self.c4.position = pygame.Vector2(1020, 520)
            self.c4.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP4.png')
            self.Cars.append(self.c4)

        for c in self.Cars:
            c.collider = pygame.Rect(c.position.x-20, c.position.y-20, 100,190)
            c.rb = pygame.Rect(c.position.x, c.position.y, 60,150)

    def playerStatusReset(self):
        for p in self.Players:
            p.status = 0
            p.scoreText = ""

    ### Resets player location to starting point
    def playerLocReset(self):
        if Preferences.RED_PLAYER_TYPE == "Player":
            self.p1.position = pygame.Vector2(140,470)
        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.p2.position = pygame.Vector2(340,470)
        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.p3.position = pygame.Vector2(750,470)
        if Preferences.GREEN_PLAYER_TYPE == "Player":
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
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")

    ##### Run Game Loop #####
    def run(self):
        self.update() 
        self.render()

    ##### Update Game #####
    def update(self):
        self.inputManager()
        # self.lastRoundCheck()
        self.readyCheck()

    ##### Render Game #####
    def render(self):
        ### Fill Background ###
        self.screen.fill((255,255,255))
        ### Set Background Image ###

        self.screen.blit(self.loadingScreen, (0,0))

        ##### DEBUG / STATUS #####

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
                self.GAME_FONT.render_to(self.screen, (200, 430), " !!POLICE HAVE ARRIVED, ALL PLAYERS STILL IN LOSE THEIR SAVINGS !!", (255, 255, 255))
        # self.GAME_FONT.render_to(self.screen, (10, 370), "Press Num key for player (P1 == 1) to cash out of the round", (0, 0, 0))
        # self.GAME_FONT.render_to(self.screen, (10, 395), "Press S for scene selection", (0, 0, 0))

        # self.GAME_FONT.render_to(self.screen, (10, 480), "Round:", (0, 0, 0))
        # self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore)+"   P2: "+str(self.p2.tmpScore)+"   P3: "+str(self.p3.tmpScore)+"   P4: "+str(self.p4.tmpScore), (0, 0, 0))
        # self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore), (0, 0, 0))

        # self.GAME_FONT.render_to(self.screen, (10, 520), "Score:", (0, 0, 0))
        # self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score), (0, 0, 0))
        # self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score)+"   P2: "+str(self.p2.score)+"   P3: "+str(self.p3.score)+"   P4: "+str(self.p4.score), (0, 0, 0))

        # self.GAME_FONT.render_to(self.screen, (350, 20), "HIGHEST SCORE PAST "+str(self.winScore)+" WINS", (0, 0, 0))
        if self.lastRound:
            self.GAME_FONT.render_to(self.screen, (350, 50), self.result, (0, 0, 0))

        ##### STORE COLLIDERS #####
        ### checks for any players colliding with the store col, adds them to the store if they're not in yet
        for s in self.Stores:
            for p in self.Players:
                if p.status != -1:
                    collide = s.collider.colliderect(p.collider)
                    if s.status != -1:
                        if collide:
                            if p not in s.players:
                                s.players.append(p)

                            # self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-20), "Ready?", (0, 0, 0))

                        else:
                            if len(s.players) == 0:
                                s.color = (0, 0, 255)
                            if p in s.players:
                                s.players.remove(p)
                                p.status = 0

        ##### CAR COLLIDERS #####
        ### check for specified player's colision, sets option for cash out if collision is true
        for c in self.Cars:
            # pygame.draw.rect(self.screen, (255,255,255), c.collider)
            # pygame.draw.rect(self.screen, (255,0,0), c.rb)
            self.screen.blit(c.carSprite, c.position)
            for p in self.Players:
                if c.playerNum == p.playerNum:
                    collide = c.collider.colliderect(p.collider)
                    if collide and p.status != -1:
                        c.ready = True
                        self.GAME_FONT.render_to(self.screen, (c.position.x+10, c.position.y-85), "P"+str(p.playerNum), (255,255,255))
                        self.GAME_FONT.render_to(self.screen, (c.position.x-60, c.position.y-60), "SELECT to Cash-Out", (255,255,255))

                    else:
                        c.ready = False

        ##### STORES #####

        # pygame.draw.rect(self.screen, (255,255,255), (160, 0, 950, 290))

        # pygame.draw.rect(self.screen, (255,255,255), (170, 0, 940, 270))

        #for s in self.Stores:
            # pygame.draw.rect(self.screen, s.color, (s.position.x, s.position.y, 40,40))
            # needs to clear each round
            #self.GAME_FONT.render_to(self.screen, (s.position.x-101, s.position.y-296), s.scoreText, (255,255,255))
            #self.GAME_FONT.render_to(self.screen, (s.position.x-100, s.position.y-295), s.scoreText, s.scoreTextColor)

        ##### PLAYERS #####
        for p in self.Players:
            if p.status != -1:
                # pygame.draw.circle(self.screen, p.color , p.position, 20)
                # pygame.draw.rect(self.screen, (255,255,0), p.XCol)
                # pygame.draw.rect(self.screen, (0,0,255), p.YCol)

                ### Collider Visualization ###

                # Render sprite
                if p.status == 0:
                    for action_name, sprite in self.character_sprites[p.character].items():
                        # Check if this action is the last updated action for this character
                        if action_name == self.character_sprites[p.character]["last_action"]:
                            # Render the last updated sprite
                            adjusted_position = p.position - pygame.Vector2(30, 50)
                            self.screen.blit(sprite.current_sprite, adjusted_position)

        # runs the status updates for all dynamic objects

        self.status()

        pygame.display.flip()

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

    ### displays the status of players and stores
    def status(self):
        for s in self.Stores:
            # self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-80), "Store "+str(s.storeNum), (0, 0, 0))
            if s.status == -1:
                s.color = (255,0,0)
            else:
                
                offset = 0
                for x in range(s.risk):
                    self.screen.blit(self.badgeSprite, (s.position.x+10+offset, s.position.y-280))
                    offset = offset+20
                self.GAME_FONT.render_to(self.screen, (s.position.x-100, s.position.y-270), "Risk: ", (255, 255, 255))

                offset = 0
                for x in range(s.risk):
                    self.screen.blit(self.moneySprite, (s.position.x+10+offset, s.position.y-250))
                    offset = offset+20
                self.GAME_FONT.render_to(self.screen, (s.position.x-100, s.position.y-240), "Reward: ", (255, 255, 255))
                
                offset = 0
                for p in s.players:
                    if p.status == 1:
                        s.scoreText = ""
                        self.GAME_FONT.render_to(self.screen, (s.position.x-101+offset, s.position.y-301), "P"+str(p.playerNum), (255,255,255))
                        self.GAME_FONT.render_to(self.screen, (s.position.x-100+offset, s.position.y-300), "P"+str(p.playerNum), p.color)
                        offset = offset + 40


        for p in self.Players:
            self.GAME_FONT.render_to(self.screen, (p.gr.x-18, p.gr.y-42), "$"+str(p.score), (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-40), "$"+str(p.score), (255, 255, 255))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-18, p.gr.y-22), "P"+str(p.playerNum), (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-20), "P"+str(p.playerNum), (255, 255, 255))


            self.GAME_FONT.render_to(self.screen, (p.gr.x-18, p.gr.y+8), "Mods" , (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y+10), "Mods" , Settings.COLOR_TEXT)
            offset = 0
            for m in p.currentMods:
                offset = offset + 20
                self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y+8+offset), m.name , (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y+10+offset), m.name , (255, 255, 255))

            #self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-60), "$"+str(p.tmpScore), (150, 150, 150))

            # self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-60), "$"+str(p.tmpScore), (150, 150, 150))


            if p.status == 0:
                printTemp = round(p.tmpScore+p.score, 2)
                self.GAME_FONT.render_to(self.screen, (p.position.x-18, p.position.y+18), "$"+str(p.tmpScore), (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+20), "$"+str(p.tmpScore), (255, 255, 255))
                self.GAME_FONT.render_to(self.screen, (p.position.x-18, p.position.y+38), "$"+str(printTemp), (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+40), "$"+str(printTemp), (175, 175, 175))
                self.GAME_FONT.render_to(self.screen, (p.position.x-13, p.position.y-68), "P"+str(p.playerNum), (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-15, p.position.y-70), "P"+str(p.playerNum), (255, 255, 255))
                self.GAME_FONT.render_to(self.screen, (p.position.x-18, p.position.y+58), p.scoreText, (0,0,0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+60), p.scoreText, (0,255,0))

            # stoplight status
            '''
            pygame.draw.circle(self.screen, "black" , p.gr, 10)
            pygame.draw.circle(self.screen, "black" , p.yl, 10)
            pygame.draw.circle(self.screen, "black" , p.rd, 10)

            if p.status == -1:
                pygame.draw.circle(self.screen, "red" , p.rd, 10)
            elif p.status == 0:
                pygame.draw.circle(self.screen, "yellow" , p.yl, 10)
            elif p.status == 1:
                pygame.draw.circle(self.screen, "green" , p.gr, 10)
            '''

    ##### Game Functions #####

    ### handles all inputs for the game ###
    def inputManager(self):
        if self.statusFlag:
            print("Scene1")
            self.resetRound()
            self.scene_manager.switch_scene('status')

        dt = self.clock.tick(60) / 1000

        ##### Player Controls #####

        if not self.police:
            for p in self.Players:
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
                            # DEBUG STATEMENT
                            if p.playerNum == 1:
                                print("space pressed...")
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

            # if event.type == pygame.JOYDEVICEADDED:
            #     controller = pygame.joystick.Joystick(event.device_index)
            #     self.controllers.append(controller)

            
    def handle_dice_roll(self):
        # DEBUG STATEMENT
        print("handle_dice_roll() called...")
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
                                print("Default Roll Started")
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

    def handle_ready_action(self, player):
        for c in self.Cars:
            ##### if at car cash out
            if c.ready and c.playerNum == player.playerNum:
                player.score = player.score + player.tmpScore
                player.tmpScore = 0
                player.status = -1
                self.Cars.remove(c)
                self.roundCheck()
            else:
        #### if at store, set to ready
                for s in self.Stores:
                    if player in s.players:
                        if player.status != -1:
                            player.status = 1

    def policeRoll(self, store):
        print("Police Roll")
        self.resetTempScores()
        store.scoreText = "POLICE"
        store.scoreTextColor = (255,0,0)
        store.status = -1
        self.police = True
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

    def alarmedStoreRoll(self, store):
        store.scoreText = "ALARMED"
        store.scoreTextColor = (255,0,0)
        self.alarmedStores = self.alarmedStores + 1
        store.status=-1

        for p in store.players:
            p.status = 0
            p.scoreText = ""
            p.streak = 0
            if modifier.quick_hands not in p.currentMods:
                p.tmpScore = 0
            else:
                del p.currentMods[modifier.quick_hands]

            if modifier.lucky_streak in p.currentMods:
                del p.currentMods[modifier.lucky_streak]
                p.streak = 0

        store.players.clear()
    
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
                
                p.tmpScore = round(p.tmpScore, 2)
                printScore = round(printScore, 2)
                p.status = 0
                p.scoreText = "+"+str(printScore)
                store.scoreTextColor = (0,255,0)
                print("Default Roll Finished")

    def boundaryCollision(self, player, tempX, tempY, locX, locY):
        # print("Loc: "+str(tempX)+" "+str(tempY)+" "+str(locX)+" "+str(locY))

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

    ### handles rolls, num 1 is the lowest number, num2 is highest number, risk is the level of risk mod applied, reward is the level of reward mod applied
    def roll(self, num1, num2, riskMod, rewardMod):
        self.roll1 = random.randint(num1, num2-(riskMod-1))
        self.roll2 = random.randint(num1, num2-(riskMod-1))
        if self.roll1 == self.roll2:
            return -1
        else: 
            return (self.roll1+self.roll2)*self.rewardScale(rewardMod)

    ### handles the reward scaling
    def rewardScale(self, rewardMod):
        match rewardMod:
            case 1:
                return 1.0
            case 2:
                return 1.5
            case 3:
                return 2.0
            case 4:
                return 3.0
            case 5:
                return 5.0

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


    ### handles snake eyes roll ##
    def snakeEyes(self):

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
        # else:
        # self.gameOver()


    def resetTempScores(self):
        for p in self.Players:
            p.tmpScore = 0

    ### get's num of active players
    def activePlayers(self):
        count = 0
        for p in self.Players:
            if p.status != -1:
                count = count +1

        return count

    def lastRoundCheck(self):
        if not self.lastRound:
            for p in self.Players:
                if p.score >= self.winScore:
                    if self.activePlayers() > 0:
                        self.lastRound = True
                        self.result = "LAST ROUND"
                    else:
                        self.gameOver()

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
        self.roundSkipped = False
        self.scene_manager.switch_scene('status')
        # print("Scene2")


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
        self.gameOverFlag = False
        self.statusFlag = True
        self.roundSkipped = False
