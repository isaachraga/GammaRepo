import pygame
import pygame.freetype  # Import the freetype module.
import random
from settings import Settings
import math

### BUGS ###
# players cant move while touching a boundary
# need to set up police roll
# if store gets alarmed and last turn, players still have a chance to win


### FEATURES ###
# need to set up police roll once an alarm has been triggered

##### CONTROLS #####
#P1 Controls - wasd/1-confirm/2-cash out
#P2 Controls - tfgh/3-confirm/4-cash out
#P3 Controls - ijkl/5-confirm/6-cash out
#P4 Controls - up left right down/7-confirm/8-cash out

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
        self.winScore = 200
        self.lastRound = False
        self.gameOverFlag = False
        self.pause = False
        self.scene = "game"
        self.ready = False
        self.allAlarms = False
        self.numPlayers = 2
        self.controllers = []
        self.statusFlag = False

        self.moveSpeed = 300

        self.playerReset()
        self.playerLocReset()
        self.storeReset()


    def storeReset(self):
        self.store1 = Store()
        self.store1.storeNum = 1
        self.store1.position = pygame.Vector2(300, 100)

        self.store2 = Store()
        self.store2.storeNum = 2
        self.store2.position = pygame.Vector2(500, 100)

        self.store3 = Store()
        self.store3.storeNum = 3
        self.store3.position = pygame.Vector2(700, 100)
        
        self.store4 = Store()
        self.store4.storeNum = 4
        self.store4.position = pygame.Vector2(900, 100)
        

        self.Stores = [self.store1,self.store2,self.store3, self.store4]

        for s in self.Stores:
            s.collider = pygame.Rect(s.position.x, s.position.y, 20,20)


    def playerReset(self):
        self.p1 = Player()
        self.p1.playerNum = 1
        self.p1.up = pygame.K_w
        self.p1.down = pygame.K_s
        self.p1.left = pygame.K_a
        self.p1.right = pygame.K_d
        self.p1.ready = pygame.K_1
        self.p1.cashOut = pygame.K_2 
        self.p1.color = (255,0,0)
        self.p1.gr = pygame.Vector2(30,60)
        self.p1.yl = pygame.Vector2(30,80)
        self.p1.rd = pygame.Vector2(30,100)

        self.p2 = Player()
        self.p2.playerNum = 2
        self.p2.up = pygame.K_t
        self.p2.down = pygame.K_g
        self.p2.left = pygame.K_f
        self.p2.right = pygame.K_h
        self.p2.ready = pygame.K_3
        self.p2.cashOut = pygame.K_4
        self.p2.color = (0,0,255)
        self.p2.gr = pygame.Vector2(1250,60)
        self.p2.yl = pygame.Vector2(1250,80)
        self.p2.rd = pygame.Vector2(1250,100)
        '''
        self.p3 = Player()
        self.p3.playerNum = 3
        self.p3.up = pygame.K_i
        self.p3.down = pygame.K_k
        self.p3.left = pygame.K_j
        self.p3.right = pygame.K_l
        self.p3.ready = pygame.K_5
        self.p3.cashOut = pygame.K_6
        self.p3.color = (0,255,0)
        self.p3.gr = pygame.Vector2(30,260)
        self.p3.yl = pygame.Vector2(30,280)
        self.p3.rd = pygame.Vector2(30,300)
        
        self.p4 = Player()
        self.p4.playerNum = 4
        self.p4.up = pygame.K_UP
        self.p4.down = pygame.K_DOWN
        self.p4.left = pygame.K_LEFT
        self.p4.right = pygame.K_RIGHT
        self.p4.ready = pygame.K_7
        self.p4.cashOut = pygame.K_8
        self.p4.color = (0,255,255)
        self.p4.gr = pygame.Vector2(1250,260)
        self.p4.yl = pygame.Vector2(1250,280)
        self.p4.rd = pygame.Vector2(1250,300)
        '''
        

        #self.Players = [self.p1, self.p2, self.p3, self.p4]
        self.Players = [self.p1,self.p2]

    def playerLocReset(self):
        self.p1.position = pygame.Vector2(500,500)
        self.p2.position = pygame.Vector2(700,500)
        #self.p3.position = pygame.Vector2(900,500)
        #self.p4.position = pygame.Vector2(1100,500)

    ##### Run Game Loop #####
    def run(self):
        self.update() # render game
        self.render()

    ##### Update Game #####
    def update(self):
        self.roundCheck()
        self.inputManager()
        self.lastRoundCheck()
        self.readyCheck()
        

    ##### Render Game #####
    def render(self):
        self.screen.fill((255,255,255))

        
        
        
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
            self.GAME_FONT.render_to(self.screen, (s.position.x, s.position.y-60), s.scoreText, (0, 0, 0))

        ##### PLAYERS #####
        for p in self.Players:
            if p.status != -1:
                pygame.draw.circle(self.screen, p.color , p.position, 20)

        
        self.status()
        
        
        ##### DEBUG #####
        #self.GAME_FONT.render_to(self.screen, (10, 10), "Dice 1: "+str(self.num1), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 30), "Dice 2: "+str(self.num2), (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 380), self.result, (0, 0, 0))

        if self.ready:
            self.GAME_FONT.render_to(self.screen, (10, 350), "Press SPACE to roll", (0, 0, 0))
        else:
            self.GAME_FONT.render_to(self.screen, (10, 350), "Waiting for Players", (0, 0, 0))
        
        #self.GAME_FONT.render_to(self.screen, (10, 370), "Press Num key for player (P1 == 1) to cash out of the round", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 395), "Press S for scene selection", (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 480), "Round:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore)+"   P2: "+str(self.p2.tmpScore)+"   P3: "+str(self.p3.tmpScore)+"   P4: "+str(self.p4.tmpScore), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore), (0, 0, 0))
        
        #self.GAME_FONT.render_to(self.screen, (10, 520), "Score:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score)+"   P2: "+str(self.p2.score)+"   P3: "+str(self.p3.score)+"   P4: "+str(self.p4.score), (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 580), "Finishline Score: "+str(self.winScore)+" (Highest Score Past Finish Line Wins!)", (0, 0, 0))
        
        pygame.display.flip()

    def readyCheck(self):
        for p in self.Players:
            if p.status != 0:
                self.ready = True
            else:
                self.ready = False

    def status(self):
        for s in self.Stores:
            self.GAME_FONT.render_to(self.screen, (s.position.x-20, s.position.y-40), "Store "+str(s.storeNum), (0, 0, 0))
            if s.status == -1:
                s.color = (255,0,0)
                

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
        dt = self.clock.tick(60) / 1000

        
        keys = pygame.key.get_pressed()
        
        
        pygame.joystick.init()  #Initialize joystick module
        

        ## need boundaries


        ##### Player Controls #####
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

                    if self.statusFlag:
                        self.scene_manager.switch_scene('status')

                    #check for all alarms
                    count = 0
                    for s in self.Stores:
                        if s.status == -1:
                            count = count + 1
                    
                    if count == len(self.Stores):
                        self.allAlarms = True

                        
                    if self.gameOverFlag:
                        self.snakeEyes()
                    elif self.allAlarms:
                        self.resetGame()
                    else: 
                        if self.ready:
                            #dice-eventually modular values
                            for s in self.Stores:
                                if len(s.players) != 0:
                                    
                                    s.num1 = random.randint(1, 6)
                                    s.num2 = random.randint(1, 6)

                                    if s.num1==s.num2:
                                        if s.num1 == 1:
                                            s.scoreText = "!POLICE!"
                                            if not self.lastRound:
                                                self.result = "SNAKE EYES"
                                                for p in self.Players:
                                                    p.tmpScore = 0
                                                    if p.status == 1:
                                                        p.score = 0
                                                    p.status = -1
                                            else:
                                                for p in self.Players:
                                                    p.tmpScore = 0
                                                    if p.status == 1:
                                                        p.score = 0
                                                    p.status = -1
                                                    
                                                    
                                        else:
                                            s.scoreText = "!ALARMED!"
                                            s.status=-1
                                            if not self.lastRound:
                                                self.result = "RESET"
                                                for p in s.players:
                                                    p.status = 0
                                                    p.tmpScore = 0
                                                    
                                            else:
                                                for p in s.players:
                                                    p.status = -1
                                                    p.tmpScore = 0
                                            s.players.clear()
                                                    

                                    else:
                                        self.result = ""
                                        for p in s.players:
                                            if p.status == 1:
                                                p.tmpScore = p.tmpScore+s.num1+s.num2
                                                p.status = 0
                                                s.scoreText = "+"+str(s.num1+s.num2)
                                    

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
                
                
                # Scene Selection
                

                # keys when shift is held for scene selection
                mods = pygame.key.get_mods()
                shift_held = mods & pygame.KMOD_SHIFT

                if shift_held: 
                    if event.key == pygame.K_s:
                        self.scene_manager.switch_scene("pause")

            if event.type == pygame.JOYDEVICEADDED:
                controller = pygame.joystick.Joystick(event.device_index)
                self.controllers.append(controller)
    
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
                    self.storeReset()
                    self.playerLocReset()
            else:
                count = 0
                self.gameOver()
            self.statusFlag = True
            
        
        

    def snakeEyes(self):
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
                    self.storeReset()
                    self.playerLocReset()
            else:
                count = 0
                self.gameOver()

    def lastRoundCheck(self):
        if not self.lastRound:
            for p in self.Players:
                if p.score >= self.winScore:
                    self.lastRound = True
                    self.result = "LAST ROUND"

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
    
    def resetGame(self):
        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        self.result = ""
        self.winScore = 50
        self.lastRound = False
        self.allAlarms = False
        self.playerReset()
        self.playerLocReset()
        self.storeReset()
        self.gameOverFlag = False

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
