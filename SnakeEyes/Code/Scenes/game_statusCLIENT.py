import pygame
import pygame_gui
import pygame.freetype
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
import socket
import threading
import pickle
import sys

class GameStatusCLIENT:
    def __init__(self, scene_manager, game, Mult):
        self.Mult = Mult
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)

        self.pNum = 2
        self.connected = False
        self.running = False
        self.assigned = False
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mstatus'

        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.clock = pygame.time.Clock() #Needed for pygame_gui

        self.make_GUI()

    def make_GUI(self):
        self.button_width = 500
        self.button_height = 70

        '''self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2)-self.button_width/2, (Settings.HEIGHT)-self.button_height), #Position
                (self.button_width, self.button_height)), #Size
            text='CONTINUE',
            manager=self.ui_manager
        )'''

        sidePadding = 25
        verticalPadding = 80
        self.back_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((sidePadding), (verticalPadding)), #Position
                (Settings.WIDTH - (sidePadding*2), Settings.HEIGHT - (verticalPadding*2))), #Size
            object_id='#back_panel',
            manager=self.ui_manager
        )
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    '''
    START OF CLIENT FUNCTIONS
    '''

    def clientInit(self, pNum, GC1, GC2):
        self.GC1 = GC1
        self.GC2 = GC2
        self.pNum = pNum
        #self.controllerHandling()
        
        while self.connected == False:
            #print("client")
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Trying to connect: "+GC1+".tcp.ngrok.io:"+GC2)
            self.c.connect((GC1+".tcp.ngrok.io",int(GC2)))
            check = self.c.recv(1024).decode()
            if check == "StatusConnected":
                print(check)
                self.c.send("Hey Serv".encode())

                self.connected = True
                self.running = True
                self.assigned = True
    '''
    def controllerHandling(self):
        if self.pNum == 2:
            self.controllerAssignment(self.player, Preferences.BLUE_CONTROLS)

        if self.pNum == 3:
            self.controllerAssignment(self.player, Preferences.YELLOW_CONTROLS)

        if self.pNum == 4:
            self.controllerAssignment(self.player, Preferences.RED_CONTROLS)
    '''
    def clientProcess(self):
        if self.running:
            try:
                #print("Running...")
                game_status = {
                    'pNum': self.pNum,
                    'Scene': self.tempScene
                }
                self.c.send(pickle.dumps(game_status))
                game_state = pickle.loads(self.c.recv(1024))
                self.dataImport(game_state)
                self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui

            except EOFError:
                print("STATUS End of Connection Client")
                print(self.tempScene)
                self.running = False
                if self.tempScene == 'mgame':
                    #print("Controlls: "+Preferences.BLUE_CONTROLS)
                    self.game.clientInit(self.pNum, self.GC1, self.GC2)
                    self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    self.closeConnection()
                    self.scene_manager.switch_scene('mgame')
                elif self.tempScene == 'mmods':
                    #print("Controlls: "+Preferences.BLUE_CONTROLS)
                    self.scene_manager.scenes['mmods'].clientInit(self.pNum, self.GC1, self.GC2)
                    self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    self.closeConnection()
                    self.scene_manager.switch_scene('m,ods')
                else:
                    self.scene_manager.switch_scene('menu')
                    self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    self.scene_manager.multiplayer_destroy()

                self.c.close()
                print("STATUS EoC Exiting...")

    def closeConnection(self):
        self.connected = False
        self.running = False
        self.assigned = False
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mstatus'

    def dataImport(self, game_state):
        self.pNum = game_state['pNum']
        self.tempScene = game_state['Scene']
    '''
    END OF CLIENT FUNCTIONS
    '''
    def run(self):
        #self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        
        self.update()
        if self.assigned:
            self.clientProcess()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.c.shutdown(socket.SHUT_RDWR)
                self.c.close()
                self.scene_manager.quit()

                #play on scene transition
                #self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)

        status_text_rect = self.HEADER_FONT.get_rect("GAME STATUS")
        status_text_rect.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, status_text_rect, "GAME STATUS", Settings.COLOR_TEXT)

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen)    

        #Score
        pCount = len(self.game.Players)

        VerticalPadding = 100
        bufferBetween = 25
        barRight = Settings.WIDTH - 150
        barLeft = 150
        minBarWidth = 10
        barGoalWidth = barRight - (barLeft + minBarWidth)
        totalHeight = Settings.HEIGHT - (VerticalPadding * 2)
        spaceForBars = totalHeight - (bufferBetween * (pCount - 1))
        barHeight = spaceForBars / pCount
        goalBarWidth = 3
        
        #Goal Bar
        goal_rect = pygame.Rect(barRight, VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_TEXT, goal_rect)

        #Intermediate bars
        intermediate_rect = pygame.Rect(barRight - ((barGoalWidth/4)*1), VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, intermediate_rect)
        intermediate_rect = pygame.Rect(barRight - ((barGoalWidth/4)*2), VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, intermediate_rect)
        intermediate_rect = pygame.Rect(barRight - ((barGoalWidth/4)*3), VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, intermediate_rect)

        #Player Bars
        pCurIndex = 1
        for p in self.game.Players:
            #Handle decimals
            pScore = float(self.game.getScore(p.playerNum))
            if (Settings.ROUNDING_PRECISION != 0):
                pScore = round(pScore, Settings.ROUNDING_PRECISION)
            else:
                pScore = int(pScore)

            #Score Bar
            curBarWidth = minBarWidth + (barGoalWidth * (pScore / Preferences.FINISHLINE_SCORE))
            # curBarWidth = minBarWidth + barGoalWidth #DEBUG
            rect = pygame.Rect( barLeft, VerticalPadding+((pCurIndex-1)*(barHeight + bufferBetween)), curBarWidth, barHeight) #x, y, width, height
            pygame.draw.rect(self.screen, p.color, rect)
            
            #Text
            player_num_text = "P"+str(p.playerNum)
            player_num_rect = self.GAME_FONT.get_rect(player_num_text)
            player_num_rect.midright = (rect.left - 5, rect.centery - Settings.FONT_SIZE/2)
            self.GAME_FONT.render_to(self.screen, player_num_rect, player_num_text, Settings.COLOR_TEXT)
            
            player_score_text = "$"+str(f'{pScore:,.{Settings.ROUNDING_PRECISION}f}')
            player_score_rect = self.GAME_FONT.get_rect(player_score_text)
            player_score_rect.midright = (rect.left - 5, rect.centery + Settings.FONT_SIZE/2)
            self.GAME_FONT.render_to(self.screen, player_score_rect, player_score_text, Settings.COLOR_TEXT)

            pCurIndex += 1

        #Goal Text
        goal_text = "Goal"
        goal_text_rect = self.GAME_FONT.get_rect(goal_text)
        goal_text_rect.midleft = (goal_rect.right + 5, goal_rect.centery - Settings.FONT_SIZE/2)
        self.GAME_FONT.render_to(self.screen, goal_text_rect, goal_text, Settings.COLOR_TEXT)

        goal_score_text = "$"+str(f'{Preferences.FINISHLINE_SCORE:,.{Settings.ROUNDING_PRECISION}f}')
        goal_score_rect = self.GAME_FONT.get_rect(goal_score_text)
        goal_score_rect.midleft = (goal_rect.right + 5, goal_rect.centery + Settings.FONT_SIZE/2)
        self.GAME_FONT.render_to(self.screen, goal_score_rect, goal_score_text, Settings.COLOR_TEXT)


        pygame.display.flip()