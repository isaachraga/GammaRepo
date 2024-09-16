import pygame
import pygame.freetype  # Import the freetype module.
import random
from settings import Settings

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

        #self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()
        self.p1.playerNum = 1
        self.p2.playerNum = 2
        self.p3.playerNum = 3
        self.p4.playerNum = 4

        self.Players = [self.p1, self.p2, self.p3, self.p4]

    ##### Run Game Loop #####
    def run(self):
        self.running = True
        while self.running:
            self.update()
            self.render()
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
        text_surface, rect = self.GAME_FONT.render("Dice 1:  "+str(self.num1), (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        # or just `render_to` the target surface.
        self.GAME_FONT.render_to(self.screen, (10, 30), "Dice 2: "+str(self.num2), (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 250), self.result, (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 350), "Press SPACE to roll", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 370), "Press Num key for player (P1 == 1) to cash out of the round", (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 480), "Round:", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 500), "P1: "+str(self.p1.tmpScore)+"   P2: "+str(self.p2.tmpScore)+"   P3: "+str(self.p3.tmpScore)+"   P4: "+str(self.p4.tmpScore), (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 520), "Score:", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 540), "P1: "+str(self.p1.score)+"   P2: "+str(self.p2.score)+"   P3: "+str(self.p3.score)+"   P4: "+str(self.p4.score), (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 580), "Finishline Score: "+str(self.winScore)+" (Highest Score Past Finish Line Wins!)", (0, 0, 0))
        
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

            self.result = "GAME OVER: Player " + str(TopPlayer.playerNum) +" Wins !\nPress Space To Restart"
    
    def resetGame(self):
        self.dt = 0
        self.num1 = 0
        self.num2 = 0
        self.result = ""
        self.winScore = 50
        self.lastRound = False
        self.gameOverFlag = False

        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()
        self.p1.playerNum = 1
        self.p2.playerNum = 2
        self.p3.playerNum = 3
        self.p4.playerNum = 4

        self.Players = [self.p1, self.p2, self.p3, self.p4]
    


########## PLAYER ##########
class Player:
    def __init__(self):
        self.tmpScore = 0
        self.score = 0
        self.stillIn = True
        self.playerNum = 0
