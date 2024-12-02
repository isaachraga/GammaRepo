import pygame
import pygame_gui
import pygame.freetype
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
import threading
import socket
import sys
import pickle

class GameStatusSERV:
    def __init__(self, scene_manager, game, Mult):
        self.Mult = Mult
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)

        self.SSH = '' #tunnel connection
        self.s = '' #socket connection
        self.running = False
        self.Clients = []
        self.tempScene = 'mstatus'

        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.clock = pygame.time.Clock() #Needed for pygame_gui

        self.make_GUI()

    def make_GUI(self):
        self.button_width = 500
        self.button_height = 70

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2)-self.button_width/2, (Settings.HEIGHT)-self.button_height), #Position
                (self.button_width, self.button_height)), #Size
            text='CONTINUE',
            manager=self.ui_manager
        )

        sidePadding = 25
        verticalPadding = 80
        self.back_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((sidePadding), (verticalPadding)), #Position
                (Settings.WIDTH - (sidePadding*2), Settings.HEIGHT - (verticalPadding*2))), #Size
            object_id='#back_panel',
            manager=self.ui_manager
        )

    '''
    START OF SERVER FUNCTIONS
    '''
    def assignTunnel(self, SSH, s, clientNum):
        #print("Blue: "+Preferences.BLUE_PLAYER_TYPE)
        self.resetConnections()
        self.SSH = SSH
        self.s = s
        clientNum = clientNum
        self.running = True
        threading.Thread(target=self.ServerListen, args=()).start()

    def ServerListen(self):
        while self.running:
            #print("SERV STATUS thread")
            try:
                self.s.settimeout(5)
                self.player = 1
                self.serverActive = True
                print("SERV STATUS Trying connection...."+str(len(self.Clients)))

                client, addr = self.s.accept()
                self.Clients.append(client)
                self.player += 1
                #self.autoPlayer()
                threading.Thread(target=self.handle_clientHOST, args=(client,self.player)).start()
            except TimeoutError:
                print("SERV STATUS Connection Timed Out")
            
        print("SERV STATUS server thread closed")
        sys.exit()

    def handle_clientHOST(self, client, pNum):
        client.send(("StatusConnected").encode())
        print(client.recv(1024).decode())
        while client in self.Clients:
            #print("running game host")
            try:
                receive = pickle.loads(client.recv(1024))
                if receive['Scene'] == 'mmods' or receive['Scene'] == 'mgame':
                    self.Clients.remove(client)
                    print("SERV STATUS client thread closed BREAK")
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    sys.exit()
                    break
                #print("Received: "+receive['msg'])
                game_state = {
                    'pNum': pNum,
                    'Scene': self.tempScene
                }
                #print("Sending...")
                client.send(pickle.dumps(game_state))
            except EOFError:
                #print("EoF HOST HC")
                self.thread = False
                #client.close()
                #self.Clients.remove(client)
            #client.send(pickle.dumps(game_state))
        #client.close()
        print("client thread closed HOST HC")
        sys.exit()

    def closeConnections(self):
        self.running = False
        for c in self.Clients:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
            self.Clients.remove(c)
            print("closed connection")

    def switchScene(self):
        while len(self.Clients) != 0:
            cl = False

    def handleSwitchScene(self):
        if Preferences.MODS_PREFERENCE == "Enabled":
            self.scene_manager.scenes['mmods'].assignTunnel(self.SSH, self.s, len(self.Clients))
            self.tempScene = 'mmods'
        else:
            print("Number of Clients"+str(len(self.Clients)))
            self.game.delayedInit()
            self.game.assignTunnel(self.SSH, self.s, len(self.Clients))
            self.tempScene = 'mgame'
            #print("^^^BLUE^^^")

        self.switchScene()
        self.running = False
        self.next_scene()

    def resetConnections(self):
        self.closeConnections()
        self.SSH = '' #tunnel connection
        self.s = '' #socket connection
        self.running = False
        self.Clients = []
        self.tempScene = 'mstatus'
    '''
    END OF SERVER FUNCTIONS
    '''

    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.closeConnections()
                self.scene_manager.quit()

            self.ui_manager.process_events(event) #Update pygame_gui

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.handleSwitchScene()
                if event.key == pygame.K_ESCAPE:
                    if self.Mult:
                        self.scene_manager.switch_scene('mpause')
                    else:
                        self.scene_manager.switch_scene('pause')
            
            if event.type == pygame.USEREVENT:
                #Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Continue Button
                    if event.ui_element == self.continue_button:
                        self.handleSwitchScene()
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def next_scene(self):
        self.resetConnections()
        if Preferences.MODS_PREFERENCE == "Enabled":
            if self.Mult:
                self.scene_manager.switch_scene('mmods')
            else:
                self.scene_manager.switch_scene('mods')
        else:
            self.game.statusFlag = False
            if self.Mult:
                self.scene_manager.switch_scene('mgame')
            else:
                self.scene_manager.switch_scene('game')

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