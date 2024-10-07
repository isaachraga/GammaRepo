import pygame
import pygame.locals
import pygame.freetype  # Import the freetype module.
import random
from settings import Settings
import math
from preferences import Preferences


### TO DO ###
# Document Code


### BUGS ###
# players cant move while touching a boundary
# dont set off police on first alarm
# last round hanling with police call/all alarms going straight to win screen
# players can walk on buildings
# quit game and restart is bugged
#


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
        
        self.tests = Tests() #automated testing

    def initialization(self):
        ### Flags and General Game Vars ###
        self.dt = 0
        self.result = ""
        self.winScore = Preferences.FINISHLINE_SCORE
        self.lastRound = False
        self.gameOverFlag = False
        self.pause = False
        self.scene = "game"
        self.ready = False
        self.allAlarms = False
        self.police = False
        self.numPlayers = 0
        self.controllers = []
        self.Cars = []
        self.Players = []
        self.statusFlag = False
        self.alarmedStores = 0
        self.testing = False

        self.moveSpeed = 300
        self.roundSkipped = False

        self.playerReset()
        self.playerLocReset()
        self.storeReset()

    ### Initializes the game after updated the preferences ###
    def delayedInit(self):
        self.winScore = Preferences.FINISHLINE_SCORE
        self.playerReset()
        self.playerLocReset()
        self.storeReset()

    ### Resets all stores to starting state ###
    def storeReset(self):
        self.store1 = Store()
        self.store1.storeNum = 1
        self.store1.position = pygame.Vector2(250, 310)
        self.assignStoreStats(self.store1)

        self.store2 = Store()
        self.store2.storeNum = 2
        self.store2.position = pygame.Vector2(500, 310)
        self.assignStoreStats(self.store2)

        self.store3 = Store()
        self.store3.storeNum = 3
        self.store3.position = pygame.Vector2(750, 310)
        self.assignStoreStats(self.store3)

        self.store4 = Store()
        self.store4.storeNum = 4
        self.store4.position = pygame.Vector2(1000, 310)
        self.assignStoreStats(self.store4)

        self.Stores = [self.store1,self.store2,self.store3, self.store4]

        for s in self.Stores:
            s.collider = pygame.Rect(s.position.x, s.position.y, 20,20)

    def playerReset(self):
        self.Players = []
        if Preferences.RED_PLAYER_TYPE == "Player":
            self.p1 = Player()
            self.p1.playerNum = 1
            self.controllerAssignment(self.p1, Preferences.RED_CONTROLS)
            self.p1.color = (255,0,0)
            self.p1.gr = pygame.Vector2(25,60)
            self.p1.yl = pygame.Vector2(25,80)
            self.p1.rd = pygame.Vector2(25,100)
            self.Players.append(self.p1)

        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.p2 = Player()
            self.p2.playerNum = 2
            self.controllerAssignment(self.p2, Preferences.BLUE_CONTROLS)
            self.p2.color = (0,0,255)
            self.p2.gr = pygame.Vector2(1210,60)
            self.p2.yl = pygame.Vector2(1210,80)
            self.p2.rd = pygame.Vector2(1210,100)
            self.Players.append(self.p2)

        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.p3 = Player()
            self.p3.playerNum = 3
            self.controllerAssignment(self.p3, Preferences.YELLOW_CONTROLS)
            self.p3.color = (204,204,0)
            self.p3.gr = pygame.Vector2(25,260)
            self.p3.yl = pygame.Vector2(25,280)
            self.p3.rd = pygame.Vector2(25,300)
            self.Players.append(self.p3)

        if Preferences.GREEN_PLAYER_TYPE == "Player":
            self.p4 = Player()
            self.p4.playerNum = 4
            self.controllerAssignment(self.p4, Preferences.GREEN_CONTROLS)
            self.p4.color = (0,255,0)
            self.p4.gr = pygame.Vector2(1210,260)
            self.p4.yl = pygame.Vector2(1210,280)
            self.p4.rd = pygame.Vector2(1210,300)
            self.Players.append(self.p4)

        self.numPlayers = len(self.Players)
        self.CarReset()


    ### Resets all carts to starting state ###
    def CarReset(self):
        self.Cars = []
        
        if Preferences.RED_PLAYER_TYPE == "Player":
            self.c1 = Car()
            self.c1.playerNum = self.p1.playerNum
            self.c1.position = pygame.Vector2(110, 520)
            self.Cars.append(self.c1)

        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.c2 = Car()
            self.c2.playerNum = self.p2.playerNum
            self.c2.position = pygame.Vector2(310, 520)
            self.Cars.append(self.c2)
        
        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.c3 = Car()
            self.c3.playerNum = self.p3.playerNum
            self.c3.position = pygame.Vector2(715, 520)
            self.Cars.append(self.c3)
        
        if Preferences.GREEN_PLAYER_TYPE == "Player":
            self.c4 = Car()
            self.c4.playerNum = self.p4.playerNum
            self.c4.position = pygame.Vector2(1020, 520)
            self.Cars.append(self.c4)

        for c in self.Cars:
            c.collider = pygame.Rect(c.position.x, c.position.y, 40,150)


    def playerStatusReset(self):
        for p in self.Players:
            p.status = 0

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
    def controllerAssignment(self, player, controlls):
        self.control_type_options = ["WASD", "TFGH", "IJKL", "Arrows", "Controller", "None"]
        match controlls:
            case "WASD":
                player.up = pygame.K_w
                player.down = pygame.K_s
                player.left = pygame.K_a
                player.right = pygame.K_d
                player.ready = pygame.K_1
                player.cashOut = pygame.K_2
            case "TFGH":
                player.up = pygame.K_t
                player.down = pygame.K_g
                player.left = pygame.K_f
                player.right = pygame.K_h
                player.ready = pygame.K_3
                player.cashOut = pygame.K_4
            case "IJKL":
                player.up = pygame.K_i
                player.down = pygame.K_k
                player.left = pygame.K_j
                player.right = pygame.K_l
                player.ready = pygame.K_5
                player.cashOut = pygame.K_6
            case "Arrows":
                player.up = pygame.K_UP
                player.down = pygame.K_DOWN
                player.left = pygame.K_LEFT
                player.right = pygame.K_RIGHT
                player.ready = pygame.K_7
                player.cashOut = pygame.K_8
            case "Controller":
                print("Error: Controller control not set up yet")
            case "None":
                print("Error: No Control Assigned")

    ##### Run Game Loop #####
    def run(self):
        self.update() 
        self.render()

    ##### Update Game #####
    def update(self):
        self.inputManager()
        self.lastRoundCheck()
        self.readyCheck()

    ##### Render Game #####
    def render(self):
        ### Fill Background ###
        self.screen.fill((255,255,255))
        ### Set Background Image ###
        self.loadingScreen = pygame.image.load('SnakeEyes/Assets/Environment/Background/Background.png')
        self.screen.blit(self.loadingScreen, (0,0))



        ##### DEBUG / STATUS #####

        #self.GAME_FONT.render_to(self.screen, (10, 10), "Dice 1: "+str(self.num1), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 30), "Dice 2: "+str(self.num2), (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 380), self.result, (0, 0, 0))
        
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
        #self.GAME_FONT.render_to(self.screen, (10, 370), "Press Num key for player (P1 == 1) to cash out of the round", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 395), "Press S for scene selection", (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 480), "Round:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore)+"   P2: "+str(self.p2.tmpScore)+"   P3: "+str(self.p3.tmpScore)+"   P4: "+str(self.p4.tmpScore), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore), (0, 0, 0))
        
        #self.GAME_FONT.render_to(self.screen, (10, 520), "Score:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score)+"   P2: "+str(self.p2.score)+"   P3: "+str(self.p3.score)+"   P4: "+str(self.p4.score), (0, 0, 0))
        
        #self.GAME_FONT.render_to(self.screen, (350, 20), "HIGHEST SCORE PAST "+str(self.winScore)+" WINS", (0, 0, 0))
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

        for s in self.Stores:
            #pygame.draw.rect(self.screen, s.color, (s.position.x, s.position.y, 40,40))
            #needs to clear each round

            self.GAME_FONT.render_to(self.screen, (s.position.x-100, s.position.y-290), s.scoreText, (255, 255, 255))

        ##### PLAYERS #####
        for p in self.Players:
            if p.status != -1:
                pygame.draw.circle(self.screen, p.color , p.position, 20)



        # runs the status updates for all dynamic objects

        self.status()

        

        pygame.display.flip()

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
                risk = ''
                for x in range(s.risk):
                    risk = risk + '* '
                self.GAME_FONT.render_to(self.screen, (s.position.x-100, s.position.y-260), "Risk: "+risk, (255, 255, 255))
                reward = ''
                for x in range(s.reward):
                    reward = reward + '$'
                self.GAME_FONT.render_to(self.screen, (s.position.x-100, s.position.y-240), "Reward: "+reward, (255, 255, 255))

        for p in self.Players:
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-40), "$"+str(p.score), (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.rd.x-20, p.rd.y+20), "P"+str(p.playerNum), (0, 0, 0))
            self.GAME_FONT.render_to(self.screen, (p.gr.x-20, p.gr.y-60), "$"+str(p.tmpScore), (150, 150, 150))

            if p.status != -1:
                self.GAME_FONT.render_to(self.screen, (p.position.x-20, p.position.y+20), "$"+str(p.tmpScore), (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (p.position.x-15, p.position.y-40), "P"+str(p.playerNum), (0, 0, 0))

            pygame.draw.circle(self.screen, "black" , p.gr, 10)
            pygame.draw.circle(self.screen, "black" , p.yl, 10)
            pygame.draw.circle(self.screen, "black" , p.rd, 10)

            if p.status == -1:
                pygame.draw.circle(self.screen, "red" , p.rd, 10)
            elif p.status == 0:
                pygame.draw.circle(self.screen, "yellow" , p.yl, 10)
            elif p.status == 1:
                pygame.draw.circle(self.screen, "green" , p.gr, 10)

    ##### Game Functions #####


    ### handles all inputs for the game ###
    def inputManager(self):
        if self.statusFlag:
            self.scene_manager.switch_scene('status')

        dt = self.clock.tick(60) / 1000

        keys = pygame.key.get_pressed()


        # pygame.joystick.init()  #Initialize joystick module

        ## need boundaries set up more precisely 


        ## need boundaries

        ##### Player Controls #####

        if not self.police:
            for p in self.Players:
                if p.status != -1:
                    tempX=0
                    tempY=0
                    if keys[p.up]:
                        tempY -= self.moveSpeed
                    if keys[p.down]:
                        tempY += self.moveSpeed
                    if keys[p.left]:
                        tempX -= self.moveSpeed
                    if keys[p.right]:
                        tempX += self.moveSpeed

                    if p.position.x + tempX < 1510 and p.position.x + tempX > -250 and p.position.y + tempY < 950 and p.position.y + tempY > -250:
                        if tempX != 0 and tempY != 0:
                            tempX = tempX*(math.sqrt(2)/2)
                            tempY = tempY*(math.sqrt(2)/2)
                        p.position.x += tempX * dt
                        p.position.y += tempY * dt
                        p.collider.center = p.position

        for event in pygame.event.get():

            ### handles application exit ###

            if event.type == pygame.QUIT:   
                self.scene_manager.quit()
                self.running = False


            if event.type == pygame.KEYDOWN:

                #### Used for Keyboard Emulation Testing // Player controls pt. 2 ####
                if self.testing:
                    if not self.police:
                        for p in self.Players:
                            if p.status != -1:
                                tempX=0
                                tempY=0
                                if event.key==p.up:
                                    tempY -= self.moveSpeed
                                if event.key==p.down:
                                    tempY += self.moveSpeed
                                if event.key==p.left:
                                    tempX -= self.moveSpeed
                                if event.key==p.right:
                                    tempX += self.moveSpeed

                                if p.position.x + tempX < 1510 and p.position.x + tempX > -250 and p.position.y + tempY < 950 and p.position.y + tempY > -250:
                                    if tempX != 0 and tempY != 0:
                                        tempX = tempX*(math.sqrt(2)/2)
                                        tempY = tempY*(math.sqrt(2)/2)
                                    p.position.x += tempX * dt
                                    p.position.y += tempY * dt
                                    p.collider.center = p.position

                # dice roller
                if event.key == pygame.K_SPACE:

                    #clear all store text
                    for s in self.Stores:
                        if s.scoreText != "!ALARMED!" and s.scoreText != "!POLICE!":
                            s.scoreText = ''

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
                                            self.resetTempScores()
                                            s.scoreText = "!POLICE!"
                                            s.status = -1
                                            self.police = True
                                            self.snakeEyes()

                                    if not self.police:
                                        # roll for value/alarm
                                        self.award = self.roll(1,9,s.risk,s.reward) 

                                        if self.award == -1:
                                            s.scoreText = "!ALARMED!"
                                            self.alarmedStores = self.alarmedStores + 1
                                            s.status=-1

                                            for p in s.players:
                                                p.status = 0
                                                p.tmpScore = 0

                                            s.players.clear()
                                        else:
                                            self.result = ""
                                            for p in s.players:
                                                if p.status == 1:
                                                    p.tmpScore = p.tmpScore+self.award
                                                    p.status = 0
                                                    s.scoreText = "+"+str(self.award)
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

                                    

                #Player Ready
                for p in self.Players:
                    if event.key == p.ready:
                        for c in self.Cars:
                            ##### if at car cash out
                            if c.ready and c.playerNum == p.playerNum:
                                p.score = p.score + p.tmpScore
                                p.tmpScore = 0
                                p.status = -1
                                self.roundCheck()
                            else:
                        #### if at store, set to ready
                                for s in self.Stores:
                                    if p in s.players:
                                        if p.status != -1:
                                            p.status = 1

                # Player Cash Out
                '''
                for p in self.Players:
                    if event.key == p.cashOut:
                        p.score = p.score + p.tmpScore
                        p.tmpScore = 0
                        p.status = -1
                        for s in self.Stores:
                            if p in s.players:
                                s.players.remove(p)
                        self.roundCheck()
                        '''

                # Scene Selection

                mods = pygame.key.get_mods()
                shift_held = mods & pygame.KMOD_SHIFT

                if shift_held: 
                    if event.key == pygame.K_s:
                        if not self.testing:
                            self.scene_manager.switch_scene("pause")
                    if event.key == pygame.K_y:
                        self.tests.run_tests(self)

            # if event.type == pygame.JOYDEVICEADDED:
            #     controller = pygame.joystick.Joystick(event.device_index)
            #     self.controllers.append(controller)

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

        store.risk = random.randint(1,5)
        store.reward = (store.risk + random.randint(1,4) - 2)

        if store.reward < 1:
            store.reward = 1
        elif store.reward > 5:
            store.reward = 5

        
    ### looks through players to see if the round is over and how to handle it ###
    def roundCheck(self):

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
            else:
                count = 0
                self.gameOver()
            self.statusFlag = True
            
            
    
        
        
    ### handles snake eyes roll ##
    def snakeEyes(self):

        for p in self.Players:
            if p.status != -1:
                p.score = 0
            # p.status = -1
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
            TopPlayer = Player()
            HighScore = 0
            for p in self.Players:
                if p.score > HighScore:
                    TopPlayer = p
                    HighScore = p.score

            self.result = "GAME OVER: Player " + str(TopPlayer.playerNum) +" Wins!\nPress Space To Restart"
            self.scene_manager.switch_scene('win')

    def resetRound(self):
        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        self.result = ""
        self.allAlarms = False
        self.police = False
        self.alarmedStores = 0
        self.playerStatusReset()
        self.resetTempScores()
        self.playerLocReset()
        self.storeReset()
        self.roundSkipped = False
        self.scene_manager.switch_scene('status')

    def resetGame(self):
        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        self.result = ""
        self.lastRound = False
        self.allAlarms = False
        self.police = False
        self.alarmedStores = 0
        self.playerReset()
        self.playerLocReset()
        self.storeReset()
        self.gameOverFlag = False
        self.statusFlag = True
        self.roundSkipped = False
        #self.scene_manager.switch_scene('status')

    def getScore(self, playerNum):
        for p in self.Players:
            if p.playerNum == playerNum:
                return str(p.score)


########## CONTROLLER ##########
class Controller:
    def __init__(self, controller_type='keyboard', controller_ID=None, controller_scheme=None):
        self.controller_type = controller_type # Can be keyboard or controller
        self.controller_ID = controller_ID # Joystick ID #'s
        self.controller_scheme = controller_scheme
        self.joystick = None

        if self.controller_type == 'joystick' and controller_ID is not None:
            self.joystick = pygame.joystick.Joystick(controller_ID)
            # self.joystick.init()  # Might be redundant?

        self.define_controlls()  # Function to define the 2 controll schemes

    def define_controlls(self):
        if self.controller_type == 'joystick':
            self.axis_horizontal = 0
            self.axis_vertical = 1
            self.action_buttons = {
                'ready': 0,
                #'cash_out': 1
            }
        elif self.controller_type == 'keyboard':
            self.map_keyboard_controls()

    def map_keyboard_controls(self):
        control_schemes = {
            "WASD": {
                "up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
                "ready": pygame.K_1,
                #"cash_out": pygame.K_2,
            },
            "TFGH": {
                "up": pygame.K_t,
                "down": pygame.K_g,
                "left": pygame.K_f,
                "right": pygame.K_h,
                "ready": pygame.K_3,
                #"cash_out": pygame.K_4,
            },
            "IJKL": {
                "up": pygame.K_i,
                "down": pygame.K_k,
                "left": pygame.K_j,
                "right": pygame.K_l,
                "ready": pygame.K_5,
                #"cash_out": pygame.K_6,
            },
            "Arrows": {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "ready": pygame.K_7,
                #"cash_out": pygame.K_8,
            },
        }
        scheme = control_schemes.get(self.control_scheme)

        if scheme:
            self.up = scheme["up"]
            self.down = scheme["down"]
            self.left = scheme["left"]
            self.right = scheme["right"]
            self.action_buttons = {
                "ready": scheme["ready"],
                #"cash_out": scheme["cash_out"],
            }
        else:
            print(f"Error: Unknown control scheme '{self.control_scheme}'")


########## PLAYER ##########
class Player:
    def __init__(self):
        self.tmpScore = 0
        self.score = 0
        self.status = 0 #-1 - cashed out | 0 - waiting | 1 ready
        self.playerNum = 0
        self.color = (255, 0, 0)
        self.position = pygame.Vector2(0, 0)
        self.collider = pygame.Rect(0,0,100,100)
        self.collider.center = self.position

        ##### STATUS #####
        self.gr = pygame.Vector2(0, 0)
        self.yl = pygame.Vector2(0, 0)
        self.rd = pygame.Vector2(0, 0)

        ##### Controlls #####
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.ready = pygame.K_1
        ##self.cashOut = pygame.K_2
        #store status locations for programatic access

class Car:
    def __init__(self):
        self.playerNum = 0
        self.position = pygame.Vector2(0, 0)
        self.collider = pygame.Rect(self.position.x, self.position.y, 60,150)
        self.ready = False

########## STORE ##########
class Store:
    def __init__(self):
        self.num1 = 0
        self.num2 = 0
        self.storeNum = 0
        self.scoreText = ""
        self.status = 0 #0 - ready | -1 alarmed
        self.color = (0,0,255)
        self.position = pygame.Vector2(0, 0)
        #risk/reward are scales that go from 1-5 that modify roll information
        self.risk = 0
        self.reward = 0
        self.collider = pygame.Rect(self.position.x, self.position.y, 20,20)
        self.players = []

########## AUTOMATED TESTING ##########
class Tests:
    
    def run_tests(self, testedClass):
        self.testedClass = testedClass
        self.testedClass.testing = True
        print("RUNNING TESTS:")
        print("- Testing Keyboard Inputs WASD")
        self.test_keyboard_inputs_wasd()
        print("- Testing Keyboard Inputs TFGH")
        self.test_keyboard_inputs_tfgh()
        print("- Testing Keyboard Inputs IJKL")
        self.test_keyboard_inputs_ijkl()
        print("- Testing Keyboard Inputs ARROWS")
        self.test_keyboard_inputs_arrows()
        print("All Tests Passed!")
        self.testedClass.testing = False

    def test_keyboard_inputs_wasd(self):
        #Testing a
        self.test_keyboard_input_left(pygame.K_a, "WASD")
        #Testing d
        self.test_keyboard_input_right(pygame.K_d, "WASD")
        #Testing w
        self.test_keyboard_input_up(pygame.K_w, "WASD")
        #Testing s
        self.test_keyboard_input_down(pygame.K_s, "WASD")
    
    def test_keyboard_inputs_tfgh(self):
        #Testing a
        self.test_keyboard_input_left(pygame.K_f, "TFGH")
        #Testing d
        self.test_keyboard_input_right(pygame.K_h, "TFGH")
        #Testing w
        self.test_keyboard_input_up(pygame.K_t, "TFGH")
        #Testing s
        self.test_keyboard_input_down(pygame.K_g, "TFGH")
    
    def test_keyboard_inputs_ijkl(self):
        #Testing a
        self.test_keyboard_input_left(pygame.K_j, "IJKL")
        #Testing d
        self.test_keyboard_input_right(pygame.K_l, "IJKL")
        #Testing w
        self.test_keyboard_input_up(pygame.K_i, "IJKL")
        #Testing s
        self.test_keyboard_input_down(pygame.K_k, "IJKL")
    
    def test_keyboard_inputs_arrows(self):
        #Testing a
        self.test_keyboard_input_left(pygame.K_LEFT, "Arrows")
        #Testing d
        self.test_keyboard_input_right(pygame.K_RIGHT, "Arrows")
        #Testing w
        self.test_keyboard_input_up(pygame.K_UP, "Arrows")
        #Testing s
        self.test_keyboard_input_down(pygame.K_DOWN, "Arrows")

        

    def test_keyboard_input_left(self, key, controller):
        self.testedClass.controllerAssignment(self.testedClass.Players[0], controller)
        location = self.testedClass.Players[0].position.x
        newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        self.testedClass.run() 
        assert(self.testedClass.Players[0].position.x < location)
        self.testedClass.playerReset()
        self.testedClass.playerLocReset()
        
    def test_keyboard_input_right(self, key, controller):
        self.testedClass.controllerAssignment(self.testedClass.Players[0], controller)
        location = self.testedClass.Players[0].position.x
        newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        self.testedClass.run() 
        
        assert(self.testedClass.Players[0].position.x > location)
        self.testedClass.playerReset()
        self.testedClass.playerLocReset()

    def test_keyboard_input_up(self, key, controller):
        self.testedClass.controllerAssignment(self.testedClass.Players[0], controller)
        location = self.testedClass.Players[0].position.y
        newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        self.testedClass.run() 
        assert(self.testedClass.Players[0].position.y < location)
        self.testedClass.playerReset()
        self.testedClass.playerLocReset()

    def test_keyboard_input_down(self, key, controller):
        self.testedClass.controllerAssignment(self.testedClass.Players[0], controller)
        location = self.testedClass.Players[0].position.y
        newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        self.testedClass.run() 
        assert(self.testedClass.Players[0].position.y > location)
        self.testedClass.playerReset()
        self.testedClass.playerLocReset()
