import pygame
import pygame.freetype  # Import the freetype module.
import random
from settings import Settings
from Scenes.scene_selection import SceneSelection
from Scenes.options import Options
from Scenes.main_menu import MainMenu
from Scenes.tutorial import Tutorial
from Scenes.credits import Credits


#P1 Controls - wasd/1-confirm/2-cash out
#P2 Controls - tfgh/3-confirm/4-cash out
#P3 Controls - ijkl/5-confirm/6-cash out
#P4 Controls - up left right down/7-confirm/8-cash out

########## GAME ##########
class Game:
    ##### Initial Setup #####
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.clock = pygame.time.Clock()

        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        self.result = ""
        self.winScore = 50
        self.lastRound = False
        self.gameOverFlag = False
        self.pause = False
        self.scene = "game"

        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()
        self.p1.playerNum = 1
        self.p2.playerNum = 2
        self.p3.playerNum = 3
        self.p4.playerNum = 4

        self.Players = [self.p1, self.p2, self.p3, self.p4]

        # Scenes
        self.scene_selection = SceneSelection(self.screen)
        self.options = Options(self.screen)
        self.menu = MainMenu(self.screen)
        self.tutorial = Tutorial(self.screen)
        self.credits = Credits(self.screen)

    ##### Run Game Loop #####
    def run(self):
        self.running = True
        while self.running:
            match self.scene:
                case "game":
                    self.update() # render game
                    self.render()
                case "scene": 
                    self.scene_selection.render()
                case "options":
                    self.options.render()
                case "tutorial":
                    self.tutorial.render()
                case "menu":
                    self.menu.render()
                case "credits":
                    self.credits.render()
                case _:
                    self.update()
                    self.render()
            
            self.inputManager()  # Always check for input events
        
        pygame.quit()

    ##### Update Game #####
    def update(self):
        self.roundCheck()
        self.inputManager()
        self.lastRoundCheck()

    ##### Render Game #####
    def render(self):
        self.screen.fill((255,255,255))
        # You can use `render` and then blit the text surface ...
        #text_surface, rect = self.GAME_FONT.render("Dice 1:  "+str(self.num1), (0, 0, 0))
        #self.screen.blit(text_surface, (10, 10))
        # or just `render_to` the target surface.
        #self.GAME_FONT.render_to(self.screen, (10, 30), "Dice 2: "+str(self.num2), (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 250), self.result, (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 350), "Press SPACE to roll", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 370), "Press Num key for player (P1 == 1) to cash out of the round", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 395), "Press S for scene selection", (0, 0, 0))

        #self.GAME_FONT.render_to(self.screen, (10, 480), "Round:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore)+"   P2: "+str(self.p2.tmpScore)+"   P3: "+str(self.p3.tmpScore)+"   P4: "+str(self.p4.tmpScore), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 520), "Score:", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score)+"   P2: "+str(self.p2.score)+"   P3: "+str(self.p3.score)+"   P4: "+str(self.p4.score), (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 580), "Finishline Score: "+str(self.winScore)+" (Highest Score Past Finish Line Wins!)", (0, 0, 0))
        
        pygame.display.flip()

    ##### Game Functions #####
    def inputManager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.running = False

            if event.type == pygame.KEYDOWN:
                #dice roller
                if event.key == pygame.K_SPACE:
                    if self.gameOverFlag:
                        self.resetGame()
                    else: 
                        #dice-eventually modular values
                        self.num1 = random.randint(1, 6)
                        self.num2 = random.randint(1, 6)

                        if self.num1==self.num2:
                            if self.num1 == 1:
                                if not self.lastRound:
                                    self.result = "SNAKE EYES"
                                    for p in self.Players:
                                        p.tmpScore = 0
                                        if p.stillIn is True:
                                            p.score = 0
                                        else:
                                            p.stillIn = True
                                else:
                                    for p in self.Players:
                                        p.tmpScore = 0
                                        if p.stillIn is True:
                                            p.score = 0
                                            p.stillIn = False
                                        
                            else:
                                if not self.lastRound:
                                    self.result = "RESET"
                                    for p in self.Players:
                                        p.stillIn = True
                                        p.tmpScore = 0
                                else:
                                    for p in self.Players:
                                        p.stillIn = False
                                        p.tmpScore = 0

                        else:
                            self.result = ""
                            for p in self.Players:
                                if p.stillIn is True:
                                    p.tmpScore = p.tmpScore+self.num1+self.num2

                #Player 1 Cash Out
                if event.key == pygame.K_1:
                    self.p1.score = self.p1.score + self.p1.tmpScore
                    self.p1.tmpScore = 0
                    self.p1.stillIn = False
                
                #Player 2 Cash Out
                if event.key == pygame.K_2:
                    self.p2.score = self.p2.score + self.p2.tmpScore
                    self.p2.tmpScore = 0
                    self.p2.stillIn = False
                
                #Player 3 Cash Out
                if event.key == pygame.K_3:
                    self.p3.score = self.p3.score + self.p3.tmpScore
                    self.p3.tmpScore = 0
                    self.p3.stillIn = False

                #Player 4 Cash Out  
                if event.key == pygame.K_4:
                    self.p4.score = self.p4.score + self.p4.tmpScore
                    self.p4.tmpScore = 0
                    self.p4.stillIn = False

                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene = "scene"

                # keys when shift is held for scene selection
                mods = pygame.key.get_mods()
                shift_held = mods & pygame.KMOD_SHIFT

                if shift_held: 
                    if event.key == pygame.K_1:
                        self.scene = "tutorial"
                    if event.key == pygame.K_2:
                        self.scene = "options"
                    if event.key == pygame.K_3:
                        self.scene = "menu"
                    if event.key == pygame.K_4:
                        self.scene = "game"
                    if event.key == pygame.K_5:
                        self.scene = "credits"

    def roundCheck(self):
        count = 0
        for p in self.Players:
            if p.stillIn == False:
                count = count + 1

        if count == 4:
            if not self.lastRound:
                for p in self.Players:
                    p.stillIn = True
                    p.tmpScore = 0
                    count = 0
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
        self.gameOverFlag = False

        self.p1 = Player()
        #self.p2 = Player()
        #self.p3 = Player()
        #self.p4 = Player()
        #self.p1.playerNum = 1
        #self.p2.playerNum = 2
        #self.p3.playerNum = 3
        #self.p4.playerNum = 4

        #self.Players = [self.p1, self.p2, self.p3, self.p4]
        self.Players = [self.p1]
    


########## PLAYER ##########
class Player:
    def __init__(self):
        self.tmpScore = 0
        self.score = 0
        #self.stillIn = True
        self.status = 0 #-1 - cashed out | 0 - waiting | 1 ready
        self.playerNum = 0
        self.locationX = 0
        self.locationY = 0

########## STORE ##########
class Store:
    def __init__(self):
        #self.stillIn = True
        self.status = 0 #0 - ready | 1 alarmed
        self.locationX = 0
        self.locationY = 0
        #risk/reward are scales that go from 1-5 that modify roll information
        self.risk = 0
        self.reward = 0
