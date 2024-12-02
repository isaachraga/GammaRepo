import pygame
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code import modifier
import threading
import pickle
import sys
import socket
#import textwrap

class GameModsSERV:
    def __init__(self, scene_manager, game, Mult):
        self.Mult = Mult
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.available_mods = modifier.available_modifiers

        self.SSH = '' #tunnel connection
        self.s = '' #socket connection
        self.running = False
        self.Clients = []
        self.tempScene = 'mmods'
        
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    
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
                print("SERV MOD Trying connection...."+str(len(self.Clients)))

                client, addr = self.s.accept()
                self.Clients.append(client)
                self.player += 1
                #self.autoPlayer()
                threading.Thread(target=self.handle_clientHOST, args=(client,self.player)).start()
            except TimeoutError:
                print("SERV MOD Connection Timed Out")
            
        print("SERV MOD server thread closed")
        sys.exit()

    def handle_clientHOST(self, client, pNum):
        client.send(("ModsConnected").encode())
        print(client.recv(1024).decode())
        while client in self.Clients:
            #print("running game host")
            try:
                receive = pickle.loads(client.recv(1024))
                self.getData(receive['pNum'], receive)
                if receive['Scene'] == 'mgame':
                    self.Clients.remove(client)
                    print("SERV MOD client thread closed BREAK")
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    sys.exit()
                    break
                #print("Received: "+receive['msg'])
                game_state = {
                    'pNum': pNum,
                    'Players': self.game.Players,
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
        print("SERV MOD client thread closed HOST HC")
        sys.exit()

    def getData(self, pNum, game_state):
        if pNum == 2:
            self.game.Players[1].right = game_state['right']
            self.game.Players[1].left = game_state['left']
            self.game.Players[1].mReadyKey = game_state['select']
        elif pNum == 3:
            self.game.Players[2].right = game_state['right']
            self.game.Players[2].left = game_state['left']
            self.game.Players[2].mReadyKey = game_state['select']
        elif pNum == 4:
            self.game.Players[3].right = game_state['right']
            self.game.Players[3].left = game_state['left']
            self.game.Players[3].mReadyKey = game_state['select']

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
        self.tempScene = 'mmods'

    def next_scene(self):
        self.resetConnections()
        
        self.game.statusFlag = False
        if self.Mult:
            self.scene_manager.switch_scene('mgame')
        else:
            self.scene_manager.switch_scene('game')
    '''
    END OF SERVER FUNCTIONS
    '''

    def run(self):
        self.update()
        self.render()

    def update(self):
        self.input_manager()
        self.input_manager_online()
        

    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)
        self.GAME_FONT.render_to(self.screen, (10, 20), "Game Mods", Settings.COLOR_TEXT)

        for p in self.game.Players:
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 50), "Player "+str(p.playerNum)+": $"+str(f'{p.score:,.{Settings.ROUNDING_PRECISION}f}'), Settings.COLOR_TEXT)
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 70), "Available Mods ", Settings.COLOR_TEXT)
            self.screen.blit(self.available_mods[p.modSelection].image, (75+(300*(p.playerNum-1)), 90))
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 150), self.available_mods[p.modSelection].name, Settings.COLOR_TEXT)
            #self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 340), modifier.available_modifiers[p.modSelection].description, Settings.COLOR_TEXT)
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 190), "$"+str(f'{round(self.available_mods[p.modSelection].cost, 2):,.{Settings.ROUNDING_PRECISION}f}'), Settings.COLOR_TEXT)
            #self.drawText(self.screen, modifier.available_modifiers[p.modSelection].description, pygame.Rect(80+(300*(p.playerNum-1)), 340, 300, 300), self.GAME_FONT)
            offset = 0
            send = ''
            for line in self.available_mods[p.modSelection].description:
                send = send + line
                if(line == '\n'):
                    self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), send , Settings.COLOR_TEXT)
                    offset = offset + 20
                    send = ''
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), send , Settings.COLOR_TEXT)
            offset = offset + 40
            if self.available_mods[p.modSelection] in p.currentMods:
                self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), "PURCHASED" , Settings.COLOR_TEXT)

            offset = offset + 80
            self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), "Current Mods" , Settings.COLOR_TEXT)
            offset = offset + 20
            Xoffset = 0
            for m in p.currentMods:
                modImg = m.image
                modImg = pygame.transform.scale(m.image, (30,30))
                self.screen.blit(modImg, (80+(300*(p.playerNum-1))+Xoffset, 230+offset))
                Xoffset = Xoffset + 40
                #self.GAME_FONT.render_to(self.screen, (80+(300*(p.playerNum-1)), 230+offset), m.image , Settings.COLOR_TEXT)

            

        self.GAME_FONT.render_to(self.screen, (350, 680), "Press SPACE to continue...", Settings.COLOR_TEXT)
        pygame.display.flip()

    def input_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.running = False
                    self.closeConnections()
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                for p in self.game.Players:
                    if p.controller:
                        if p.controller.controller_type == "keyboard" or p.controller.controller_type == "joystick":
                            if event.key == p.controller.left:
                                    #print(str(len(self.available_mods)))
                                    if(p.modSelection - 1 < 0):
                                        p.modSelection = len(self.available_mods) -1 
                                    else:
                                        p.modSelection = p.modSelection -1
                            if event.key == p.controller.right:
                                if(p.modSelection == len(self.available_mods) - 1):
                                    p.modSelection = 0
                                else:
                                    p.modSelection = p.modSelection + 1

                            if p.controller.controller_type == 'keyboard':
                                # Scene Selection
                                if event.key == pygame.K_ESCAPE:
                                    if self.Mult:
                                        self.scene_manager.switch_scene('mpause')
                                    else:
                                        self.scene_manager.switch_scene('pause')
                                
                                if event.key == p.controller.action_buttons.get('space'):
                                    self.game.statusFlag = False
                                    if self.Mult:
                                        self.handleSwitchScene()
                                    else:
                                        self.scene_manager.switch_scene('game')

                                if event.key == p.controller.action_buttons.get('ready') and p.score >= self.available_mods[p.modSelection].cost and self.available_mods[p.modSelection] not in p.currentMods:
                                    p.score = round(p.score - self.available_mods[p.modSelection].cost)
                                    p.currentMods[self.available_mods[p.modSelection]] = self.available_mods[p.modSelection]
                    
            elif event.type == pygame.JOYBUTTONDOWN:
                joystick_id = event.joy
                button_id = event.button

                for p in self.Players:
                    if p.controller.controller_type == 'joystick':
                        if p.controller.joystick.get_instance_id() == joystick_id:
                            if button_id == p.controller.action_buttons.get('space'):
                                self.game.statusFlag = False
                                if self.Mult:
                                    self.scene_manager.switch_scene('mgame')
                                else:
                                    self.scene_manager.switch_scene('game')
                            elif button_id == p.controller.action_buttons.get('ready') and p.score >= self.available_mods[p.modSelection].cost and self.available_mods[p.modSelection] not in p.currentMods:
                                p.score = round(p.score - self.available_mods[p.modSelection].cost)
                                p.currentMods[self.available_mods[p.modSelection]] = self.available_mods[p.modSelection]
    
    def input_manager_online(self):
        for p in self.game.Players:
            if not p.controller:
                #print ("Pressed: "+str(p.press))
                if p.left:
                    if not p.press:
                        p.press = True
                        if(p.modSelection - 1 < 0):
                                p.modSelection = len(self.available_mods) -1 
                        else:
                            p.modSelection = p.modSelection -1
                    

                if p.right:
                    if not p.press:
                        p.press = True
                        if(p.modSelection == len(self.available_mods) - 1):
                                p.modSelection = 0
                        else:
                            p.modSelection = p.modSelection + 1
                    

                if p.mReadyKey and p.score >= self.available_mods[p.modSelection].cost and self.available_mods[p.modSelection] not in p.currentMods:
                    if not p.press:
                        p.press = True
                        p.score = round(p.score - self.available_mods[p.modSelection].cost)
                        p.currentMods[self.available_mods[p.modSelection]] = self.available_mods[p.modSelection]
                    

                if not p.left and not p.right and not p.mReadyKey: 
                        p.press = False