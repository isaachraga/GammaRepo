import pygame
import pygame_gui
import pygame.freetype
from SnakeEyes.Code.settings import Settings
import threading
import pickle
import socket
import sys

class GameWinSERV:
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
        self.tempScene = 'mwin'


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
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")

        self.sorted_players = sorted(self.game.Players, key=lambda Player: Player.score, reverse=True)
    
    
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        self.render()

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
                print("SERV WIN Trying connection...."+str(len(self.Clients)))

                client, addr = self.s.accept()
                self.Clients.append(client)
                self.player += 1
                #self.autoPlayer()
                threading.Thread(target=self.handle_clientHOST, args=(client,self.player)).start()
            except TimeoutError:
                print("SERV WIN Connection Timed Out")
            
        print("SERV WIN server thread closed")
        sys.exit()

    def handle_clientHOST(self, client, pNum):
        client.send(("WinConnected").encode())
        print(client.recv(1024).decode())
        while client in self.Clients:
            #print("running game host")
            try:
                receive = pickle.loads(client.recv(1024))
                if receive['Scene'] == 'menu':
                    self.Clients.remove(client)
                    print("SERV WIN client thread closed BREAK")
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
        print("SERV WIN client thread closed HOST HC")
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
        self.game.delayedInit()
        self.game.assignTunnel(self.SSH, self.s, len(self.Clients))
        self.tempScene = 'menu'
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
        self.tempScene = 'mwin'

    def next_scene(self):
        self.resetConnections()
        
        self.game.statusFlag = False
        self.scene_manager.switch_scene('menu')
        self.scene_manager.multiplayer_destroy()
    '''
    END OF SERVER FUNCTIONS
    '''

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.closeConnections()
                self.scene_manager.quit()

            self.ui_manager.process_events(event) #Update pygame_gui

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.statusFlag = False
                    self.scene_manager.switch_scene('menu')
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('pause')
            
            if event.type == pygame.USEREVENT:
                #Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Continue Button
                    if event.ui_element == self.continue_button:
                        self.next_scene()
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)

        over_text_rect = self.HEADER_FONT.get_rect("GAME OVER")
        over_text_rect.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, over_text_rect, "GAME OVER", Settings.COLOR_TEXT)

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen)  

        verticalShift = 70
        bottom = Settings.HEIGHT-verticalShift
        spaceBetween = 10
        textPadding = 0.2

        wantedTextSize = 60
        titleTextSize = 22
        scoreTextSize = 50
        crimeTextSize = 25

        winnerWidth = 360
        winnerHeight = 450
        secondScale = (5/6)
        thirdScale = (4/6)
        fourthScale = (3/6)

        pCount = len(self.game.Players)

        #1st place
        if pCount >= 1:
            winner_rect = pygame.Rect((Settings.WIDTH/2)-(winnerWidth/2), (bottom/2)-(winnerHeight/2), #x, y
                            winnerWidth, winnerHeight) #width, height
            pygame.draw.rect(self.screen, (200, 200, 200), winner_rect)

            winner_text = "WANTED"
            currentFontSize = wantedTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_wanted_text_rect = currentFont.get_rect(winner_text)
            winner_wanted_text_rect.midtop = (winner_rect.centerx, winner_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_wanted_text_rect, winner_text, (0, 0, 0))
            
            winner_text = f"CRIMINAL MASTERMIND: P{self.sorted_players[0].playerNum}"
            currentFontSize = titleTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_title_text_rect = currentFont.get_rect(winner_text)
            winner_title_text_rect.midtop = (winner_wanted_text_rect.centerx, winner_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_title_text_rect, winner_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[0].character]["profile"])
            image_size = winnerWidth * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (winner_rect.centerx - (image_size/2), winner_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            winner_text = f"${self.sorted_players[0].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_score_rect = currentFont.get_rect(winner_text)
            winner_score_rect.midbottom = (winner_rect.centerx, winner_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_score_rect, winner_text, (0, 0, 0))
            
            winner_text = "For the Theft of"
            currentFontSize = crimeTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_crime_rect = currentFont.get_rect(winner_text)
            winner_crime_rect.midbottom = (winner_score_rect.centerx, winner_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_crime_rect, winner_text, (0, 0, 0))
        
        #2nd place
        if pCount >= 2:
            second_rect = pygame.Rect(0, 0, winnerWidth*secondScale, winnerHeight*secondScale) #x, y, width, height
            second_rect.bottomright = (winner_rect.left - spaceBetween, winner_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), second_rect)  

            second_text = "WANTED"
            currentFontSize = wantedTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_wanted_text_rect = currentFont.get_rect(second_text)
            second_wanted_text_rect.midtop = (second_rect.centerx, second_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_wanted_text_rect, second_text, (0, 0, 0))

            second_text = f"BURGLAR: P{self.sorted_players[1].playerNum}"
            currentFontSize = titleTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_title_text_rect = currentFont.get_rect(second_text)
            second_title_text_rect.midtop = (second_wanted_text_rect.centerx, second_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_title_text_rect, second_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[1].character]["profile"])
            image_size = winnerWidth * secondScale * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (second_rect.centerx - (image_size/2), second_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            second_text = f"${self.sorted_players[1].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_score_rect = currentFont.get_rect(second_text)
            second_score_rect.midbottom = (second_rect.centerx, second_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_score_rect, second_text, (0, 0, 0))
            
            second_text = "For the Theft of"
            currentFontSize = crimeTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_crime_rect = currentFont.get_rect(second_text)
            second_crime_rect.midbottom = (second_score_rect.centerx, second_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_crime_rect, second_text, (0, 0, 0))
        
        #3rd place
        if pCount >= 3:
            third_rect = pygame.Rect(0, 0, winnerWidth*thirdScale, winnerHeight*thirdScale) #x, y, width, height
            third_rect.bottomleft = (winner_rect.right + spaceBetween, winner_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), third_rect)  

            third_text = "WANTED"
            currentFontSize = wantedTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_wanted_text_rect = currentFont.get_rect(third_text)
            third_wanted_text_rect.midtop = (third_rect.centerx, third_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_wanted_text_rect, third_text, (0, 0, 0))

            third_text = f"THIEF: P{self.sorted_players[2].playerNum}"
            currentFontSize = titleTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_title_text_rect = currentFont.get_rect(third_text)
            third_title_text_rect.midtop = (third_wanted_text_rect.centerx, third_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_title_text_rect, third_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[2].character]["profile"])
            image_size = winnerWidth * thirdScale * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (third_rect.centerx - (image_size/2), third_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            third_text = f"${self.sorted_players[2].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_score_rect = currentFont.get_rect(third_text)
            third_score_rect.midbottom = (third_rect.centerx, third_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_score_rect, third_text, (0, 0, 0))
            
            third_text = "For the Theft of"
            currentFontSize = crimeTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_crime_rect = currentFont.get_rect(third_text)
            third_crime_rect.midbottom = (third_score_rect.centerx, third_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_crime_rect, third_text, (0, 0, 0))
        
        #4th place
        if pCount >= 4:
            fourth_rect = pygame.Rect(0, 0, winnerWidth*fourthScale, winnerHeight*fourthScale) #x, y, width, height
            fourth_rect.bottomleft = (third_rect.right + spaceBetween, third_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), fourth_rect)  

            fourth_text = "WANTED"
            currentFontSize = wantedTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_wanted_text_rect = currentFont.get_rect(fourth_text)
            fourth_wanted_text_rect.midtop = (fourth_rect.centerx, fourth_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_wanted_text_rect, fourth_text, (0, 0, 0))

            fourth_text = f"PETTY THIEF: P{self.sorted_players[3].playerNum}"
            currentFontSize = titleTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_title_text_rect = currentFont.get_rect(fourth_text)
            fourth_title_text_rect.midtop = (fourth_wanted_text_rect.centerx, fourth_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_title_text_rect, fourth_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[3].character]["profile"])
            image_size = winnerWidth * fourthScale * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (fourth_rect.centerx - (image_size/2), fourth_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            fourth_text = f"${self.sorted_players[3].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_score_rect = currentFont.get_rect(fourth_text)
            fourth_score_rect.midbottom = (fourth_rect.centerx, fourth_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_score_rect, fourth_text, (0, 0, 0))
            
            fourth_text = "For the Theft of"
            currentFontSize = crimeTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_crime_rect = currentFont.get_rect(fourth_text)
            fourth_crime_rect.midbottom = (fourth_score_rect.centerx, fourth_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_crime_rect, fourth_text, (0, 0, 0))


        pygame.display.flip()