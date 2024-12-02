import pygame
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code import modifier
from SnakeEyes.Code import controller
import socket
import pickle

#import textwrap

class GameModsCLIENT:
    def __init__(self, scene_manager, game, Mult):
        self.Mult = Mult
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.available_mods = modifier.available_modifiers

        self.pNum = 2
        self.connected = False
        self.running = False
        self.assigned = False
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mmods'
        self.left = False
        self.right = False
        self.select = False
        
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    
    def run(self):
        self.update()
        if self.assigned:
            self.clientProcess()
        self.render()

    def update(self):
        self.input_manager()
        
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
            if check == "ModsConnected":
                print(check)
                self.c.send("Hey Serv from MOD".encode())

                self.connected = True
                self.running = True
                self.assigned = True
    
    def controllerHandling(self):
        if self.pNum == 2:
            self.controllerAssignment(self.player, Preferences.BLUE_CONTROLS)

        if self.pNum == 3:
            self.controllerAssignment(self.player, Preferences.YELLOW_CONTROLS)

        if self.pNum == 4:
            self.controllerAssignment(self.player, Preferences.RED_CONTROLS)
    
    def clientProcess(self):
        if self.running:
            try:
                #print("Running...")
                game_status = {
                    'pNum': self.pNum,
                    'Scene': self.tempScene,
                    'left': self.left,
                    'right': self.right,
                    'select': self.select
                }
                self.c.send(pickle.dumps(game_status))
                game_state = pickle.loads(self.c.recv(4096))
                self.loadData(game_state)
                #self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui

            except EOFError:
                print("MODS End of Connection Client")
                print(self.tempScene)
                self.running = False
                if self.tempScene == 'mgame':
                    #print("Controlls: "+Preferences.BLUE_CONTROLS)
                    self.game.clientInit(self.pNum, self.GC1, self.GC2)
                    self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    self.closeConnection()
                    self.scene_manager.switch_scene('mgame')
                else:
                    self.scene_manager.switch_scene('menu')
                    self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    self.scene_manager.multiplayer_destroy()

                self.c.close()
                print("MODS EoC Exiting...")

    def closeConnection(self):
        self.connected = False
        self.running = False
        self.assigned = False
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mmods'
        

    def loadData(self, game_state):
        #print("Load data")
        self.pNum = game_state['pNum']
        self.Players = game_state['Players']
        if len(self.Players) == 2:
            self.p1 = self.Players[0]
            self.p2 = self.Players[1]
        elif len(self.Players) == 3:
            self.p1 = self.Players[0]
            self.p2 = self.Players[1]
            self.p3 = self.Players[2]
        elif len(self.Players) == 4:
            self.p1 = self.Players[0]
            self.p2 = self.Players[1]
            self.p3 = self.Players[2]
            self.p4 = self.Players[3]

        self.player = self.Players[self.pNum-1]
        self.controllerHandling()
        self.tempScene = game_state['Scene']

    def controllerAssignment(self, player, controls):
        #print("assigning P"+str(player.playerNum)+": " +controls)
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
        elif controls == "None":
            controller_type = "None"
            controller_ID = None
            controller_scheme = controls
            
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


    '''
    END OF CLIENT FUNCTIONS
    '''

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
        self.right = False
        self.left = False
        self.select = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                for p in self.game.Players:
                    if p.controller.controller_type == "keyboard" or p.controller.controller_type == "joystick":
                        if event.key == p.controller.left:
                            self.left = True
                        if event.key == p.controller.right:
                            self.right = True

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
                                    self.scene_manager.switch_scene('mgame')
                                else:
                                    self.scene_manager.switch_scene('game')

                            if event.key == p.controller.action_buttons.get('ready') and p.score >= self.available_mods[p.modSelection].cost and self.available_mods[p.modSelection] not in p.currentMods:
                                self.select = True

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
                                self.select = True