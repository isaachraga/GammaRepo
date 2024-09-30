import pygame
import pygame.freetype  # Import the freetype module.
import random
from settings import Settings
import math
from preferences import Preferences

### BUGS ###
# players cant move while touching a boundary
# dont set off police on first alarm
# last round hanling with police call/all alarms going straight to win screen




########## GAME ##########
class Game:
    ##### Initial Setup #####
    def __init__(self, scene_manager):
        
        self.scene_manager = scene_manager
        self.screen = scene_manager.screen
    
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.clock = pygame.time.Clock()

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
        self.numPlayers = 2
        self.controllers = []
        self.statusFlag = False
        self.alarmedStores = 0

        self.moveSpeed = 300

        self.playerReset()
        self.playerLocReset()
        self.storeReset()

    def delayedInit(self):
        self.winScore = Preferences.FINISHLINE_SCORE
        self.playerReset()
        self.playerLocReset()
        self.storeReset()

    def storeReset(self):
        self.store1 = Store()
        self.store1.storeNum = 1
        self.store1.position = pygame.Vector2(300, 400)
        self.assignStoreStats(self.store1)

        self.store2 = Store()
        self.store2.storeNum = 2
        self.store2.position = pygame.Vector2(500, 400)
        self.assignStoreStats(self.store2)

        self.store3 = Store()
        self.store3.storeNum = 3
        self.store3.position = pygame.Vector2(700, 400)
        self.assignStoreStats(self.store3)
        
        self.store4 = Store()
        self.store4.storeNum = 4
        self.store4.position = pygame.Vector2(900, 400)
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
            self.p1.gr = pygame.Vector2(30,60)
            self.p1.yl = pygame.Vector2(30,80)
            self.p1.rd = pygame.Vector2(30,100)
            self.Players.append(self.p1)

        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.p2 = Player()
            self.p2.playerNum = 2
            self.controllerAssignment(self.p2, Preferences.BLUE_CONTROLS)
            self.p2.color = (0,0,255)
            self.p2.gr = pygame.Vector2(1150,60)
            self.p2.yl = pygame.Vector2(1150,80)
            self.p2.rd = pygame.Vector2(1150,100)
            self.Players.append(self.p2)
        
        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.p3 = Player()
            self.p3.playerNum = 3
            self.controllerAssignment(self.p3, Preferences.YELLOW_CONTROLS)
            self.p3.color = (204,204,0)
            self.p3.gr = pygame.Vector2(30,260)
            self.p3.yl = pygame.Vector2(30,280)
            self.p3.rd = pygame.Vector2(30,300)
            self.Players.append(self.p3)

        if Preferences.GREEN_PLAYER_TYPE == "Player":
            self.p4 = Player()
            self.p4.playerNum = 4
            self.controllerAssignment(self.p4, Preferences.GREEN_CONTROLS)
            self.p4.color = (0,255,0)
            self.p4.gr = pygame.Vector2(1150,260)
            self.p4.yl = pygame.Vector2(1150,280)
            self.p4.rd = pygame.Vector2(1150,300)
            self.Players.append(self.p4)
        
        

        

    def playerStatusReset(self):
        for p in self.Players:
            p.status = 0

    def playerLocReset(self):
        if Preferences.RED_PLAYER_TYPE == "Player":
            self.p1.position = pygame.Vector2(450,600)
        if Preferences.BLUE_PLAYER_TYPE == "Player":
            self.p2.position = pygame.Vector2(550,600)
        if Preferences.YELLOW_PLAYER_TYPE == "Player":
            self.p3.position = pygame.Vector2(650,600)
        if Preferences.GREEN_PLAYER_TYPE == "Player":
            self.p4.position = pygame.Vector2(750,600)

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
        self.update() # render game
        self.render()

    ##### Update Game #####
    def update(self):
        self.inputManager()
        self.lastRoundCheck()
        self.readyCheck()
        

    ##### Render Game #####
    def render(self):
        self.screen.fill((255,255,255))

        ##### STORE COLLIDERS #####
        for s in self.Stores:
            for p in self.Players:
                if p.status != -1:
                    collide = s.collider.colliderect(p.collider)
                    if s.status != -1:
                        if collide:
                            s.color = (0, 255, 0)
                            if p not in s.players:
                                s.players.append(p)
                            self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-20), "Ready?", (0, 0, 0))
                            
                        else:
                            if len(s.players) == 0:
                                s.color = (0, 0, 255)
                            if p in s.players:
                                s.players.remove(p)
                                p.status = 0
                            
                
        ##### STORES #####

        for s in self.Stores:
            pygame.draw.rect(self.screen, s.color, (s.position.x, s.position.y, 40,40))
            self.GAME_FONT.render_to(self.screen, (s.position.x, s.position.y-100), s.scoreText, (0, 0, 0))

        ##### PLAYERS #####
        for p in self.Players:
            if p.status != -1:
                pygame.draw.circle(self.screen, p.color , p.position, 20)

        
        self.status()
        
        
        ##### DEBUG / STATUS #####
        #self.GAME_FONT.render_to(self.screen, (10, 10), "Dice 1: "+str(self.num1), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 30), "Dice 2: "+str(self.num2), (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 380), self.result, (0, 0, 0))
        if self.police:
                self.GAME_FONT.render_to(self.screen, (350, 120), "Press SPACE to continue...", (0, 0, 0))
        else:
            if self.ready:
                    self.GAME_FONT.render_to(self.screen, (350, 120), "Press SPACE to try your luck...", (0, 0, 0))
            else:
                self.GAME_FONT.render_to(self.screen, (350, 120), "Waiting for Players to Select a Store", (0, 0, 0))

        if self.alarmedStores > 0:
            if not self.police:
                if self.allAlarms:
                    self.GAME_FONT.render_to(self.screen, (350, 180), "All stores alarmed, time to leave the mall...", (0, 0, 0))
                else:
                    self.GAME_FONT.render_to(self.screen, (350, 180), "Police are on their way!", (0, 0, 0))
            else: 
                self.GAME_FONT.render_to(self.screen, (200, 180), " !!POLICE HAVE ARRIVED, ALL PLAYERS STILL IN LOSE THEIR SAVINGS !!", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 370), "Press Num key for player (P1 == 1) to cash out of the round", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 395), "Press S for scene selection", (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 480), "Round:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore)+"   P2: "+str(self.p2.tmpScore)+"   P3: "+str(self.p3.tmpScore)+"   P4: "+str(self.p4.tmpScore), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore), (0, 0, 0))
        
        #self.GAME_FONT.render_to(self.screen, (10, 520), "Score:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score)+"   P2: "+str(self.p2.score)+"   P3: "+str(self.p3.score)+"   P4: "+str(self.p4.score), (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (350, 20), "HIGHEST SCORE PAST "+str(self.winScore)+" WINS", (0, 0, 0))
        if self.lastRound:
            self.GAME_FONT.render_to(self.screen, (350, 50), self.result, (0, 0, 0))

        
        pygame.display.flip()


    def readyCheck(self):
        count = 0
        for p in self.Players:
            if p.status == 0:
                count = count + 1
        
        if count != 0:
            self.ready = False
        else:
            self.ready = True
           
        
    def status(self):
        for s in self.Stores:
            self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-80), "Store "+str(s.storeNum), (0, 0, 0))
            if s.status == -1:
                s.color = (255,0,0)
            else:
                risk = ''
                for x in range(s.risk):
                    risk = risk + '* '
                self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-60), "Risk: "+risk, (0, 0, 0))
                reward = ''
                for x in range(s.reward):
                    reward = reward + '$'
                self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-40), "Reward: "+reward, (0, 0, 0))
                

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
    def inputManager(self):
        if self.statusFlag:
            self.scene_manager.switch_scene('status')

        dt = self.clock.tick(60) / 1000

        
        keys = pygame.key.get_pressed()
        
        
        pygame.joystick.init()  #Initialize joystick module
        

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
            
            if event.type == pygame.QUIT:   
                self.scene_manager.quit()
                self.running = False

            if event.type == pygame.KEYDOWN:
                #dice roller
                if event.key == pygame.K_SPACE:
                    self.roundCheck()
                    #NEED LAST ROUND
                    if self.police:
                        if self.lastRound:
                            self.gameOver()
                        else:
                            self.resetRound()
                    elif self.allAlarms:
                        if self.lastRound:
                            self.gameOver()
                        else:
                            self.resetRound()
                    else: 
                        if self.ready:
                            
                            for s in self.Stores:
                                if len(s.players) != 0:
                                    #police roll
                                    if self.alarmedStores > 0:
                                        if self.roll(1,(len(self.Stores)+11-self.alarmedStores),1,1) == -1:
                                            self.resetTempScores()
                                            s.scoreText = "!POLICE!"
                                            s.status = -1
                                            self.police = True
                                            self.snakeEyes()
                                            
                                            
                                            
                                                    
                                    if not self.police:
                                        #roll for value/alarm
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
                    #check for all alarms
                    count = 0
                    for s in self.Stores:
                        if s.status == -1:
                            count = count + 1
                    
                    self.alarmedStores = count
                    
                    if count == len(self.Stores):
                        self.allAlarms = True

                                    

                #Player Ready
                for p in self.Players:
                    if event.key == p.ready:
                        for s in self.Stores:
                            if p in s.players:
                                if p.status != -1:
                                    p.status = 1

                #Player Cash Out
                for p in self.Players:
                    if event.key == p.cashOut:
                        p.score = p.score + p.tmpScore
                        p.tmpScore = 0
                        p.status = -1
                        for s in self.Stores:
                            if p in s.players:
                                s.players.remove(p)
                        self.roundCheck()
                
                
                # Scene Selection
                

                mods = pygame.key.get_mods()
                shift_held = mods & pygame.KMOD_SHIFT

                if shift_held: 
                    if event.key == pygame.K_s:
                        self.scene_manager.switch_scene("pause")

            if event.type == pygame.JOYDEVICEADDED:
                controller = pygame.joystick.Joystick(event.device_index)
                self.controllers.append(controller)

    def roll(self, num1, num2, riskMod, rewardMod):
        self.roll1 = random.randint(num1, num2-(riskMod-1))
        self.roll2 = random.randint(num1, num2-(riskMod-1))
        if self.roll1 == self.roll2:
            return -1
        else: 
            return (self.roll1+self.roll2)*self.rewardScale(rewardMod)

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
            
            
    
        
        

    def snakeEyes(self):
        
        
        for p in self.Players:
                if p.status != -1:
                    p.score = 0
                #p.status = -1
        if not self.lastRound:
            self.result = "SNAKE EYES"
        #else:
            #self.gameOver()
        

    def resetTempScores(self):
        for p in self.Players:
                p.tmpScore = 0

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
        self.scene_manager.switch_scene('status')

    def getScore(self, playerNum):
        for p in self.Players:
            if p.playerNum == playerNum:
                return str(p.score)
    


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
        self.cashOut = pygame.K_2
        #store status locations for programatic access

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
