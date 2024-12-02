import socket
import pygame
import pygame.freetype
import pygame_gui
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
import pickle


'''
remove control displays

ERRORS
assign controller type
'''


########## GAME SETUP MENU ##########
class GameSetupCLIENT:
    ##### Initial Setup #####
    def __init__(self, scene_manager, game):
        self.pNum = 2
        self.GC1 = ''
        self.GC2 = ''
        self.game = game
        self.tempScene = 'msetup2'
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json")
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)

        self.clock = pygame.time.Clock() #Needed for pygame_gui
        self.enabled = False
        

        self.makeGUI()

    def ClientSetup(self, GC1, GC2):
        self.GC1 = GC1
        self.GC2 = GC2
        print("client")
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Trying to connect: "+GC1+".tcp.ngrok.io:"+GC2)
        self.c.connect((GC1+".tcp.ngrok.io",int(GC2)))
        print(self.c.recv(1024).decode())
        self.c.send("Hey Serv from SETUP".encode())

        self.running = True
        
        
        #self.c.shutdown(socket.SHUT_RDWR)
        
        
        

    def dataImport(self, game_state):
        self.pNum = game_state['pNum']
        Preferences.FINISHLINE_SCORE = game_state['FinishlineScore']
        Preferences.MODS_PREFERENCE = game_state['ModState']
        Preferences.BLUE_PLAYER_TYPE = game_state['BluePT']
        Preferences.YELLOW_PLAYER_TYPE = game_state['YellowPT']
        Preferences.GREEN_PLAYER_TYPE = game_state['GreenPT']
        if game_state['Scene'] == 'mgame':
            print("Scene change")
            self.tempScene = 'mgame'

    def enableControls(self):
        self.enabled = True
        self.controlSchemeSelect('red', 0)
        if self.pNum == 2:
            self.controlSchemeSelect('blue', 2)
        if self.pNum == 3:
            self.controlSchemeSelect('yellow', 2)  
        if self.pNum == 4:
            self.controlSchemeSelect('green', 2)

    def makeGUI(self):
        option_select_width = 38
        option_select_height = 38
        player_option_label_width = 112
        game_option_label_width = 130
        option_label_heigth = 38

        ##########################
        ##### PLAYER OPTIONS #####
        ##########################

        self.player_type_options = ["Player", "CPU", "None"]

        if pygame.joystick.get_count() != 0:
            self.control_type_options = ["WASD", "TFGH", "IJKL", "Arrows", "Controller", "None"]
        else:
            self.control_type_options = [
                "WASD",
                "TFGH",
                "IJKL",
                "Arrows",
                "None",
            ]

        # Red Player
        self.red_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((80), (25)), #Position
                (200, 200)), #Size
            object_id='#red_panel',
            manager=self.ui_manager
        )
        # Load an image to be displayed inside the panel
        self.image_surface = pygame.image.load('SnakeEyes/Assets/Characters/Profile/Jeff Profile.png').convert_alpha()

        # Create a UIImage inside the red panel
        self.image_element = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (10, 20),  # Image position relative to the red panel
                (180, 180)),  # Image size (adjust to the size of your image)
            image_surface=self.image_surface,
            manager=self.ui_manager,
            container=self.red_panel  # Set the red panel as the container
        )

        self.red_player_index = self.player_type_options.index(Preferences.RED_PLAYER_TYPE)
        self.red_player_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((124), (251)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.red_player_index],  # Show current option
            manager=self.ui_manager
        )
        

        self.red_control_index = self.control_type_options.index(Preferences.RED_CONTROLS)
        self.red_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((124), (300)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.red_control_index],  # Show current option
            manager=self.ui_manager
        )
        

        # Blue Player
        self.blue_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((1000), (25)), #Position
                (200, 200)), #Size
            object_id='#blue_panel',
            manager=self.ui_manager
        )
        # Load an image to be displayed inside the panel
        self.image_surface = pygame.image.load('SnakeEyes/Assets/Characters/Profile/mj-profile.png').convert_alpha()

        # Create a UIImage inside the blue panel
        self.image_element = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (10, 20),  # Image position relative to the blue panel
                (180, 180)),  # Image size (adjust to the size of your image)
            image_surface=self.image_surface,
            manager=self.ui_manager,
            container=self.blue_panel  # Set the blue panel as the container
        )
        self.blue_player_index = self.player_type_options.index(Preferences.BLUE_PLAYER_TYPE)
        self.blue_player_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((1044), (251)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.blue_player_index],  # Show current option
            manager=self.ui_manager
        )

        
        self.blue_control_index = self.control_type_options.index(Preferences.BLUE_CONTROLS)
        self.blue_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((1044), (300)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.blue_control_index],  # Show current option
            manager=self.ui_manager
        )
        if self.pNum == 2:
            self.blue_control_left = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((1012), (300)), #Position
                    (option_select_width, option_select_height)),  #Size
                text='<',
                manager=self.ui_manager
            )
            self.blue_control_right = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((1156), (300)), #Position
                    (option_select_width, option_select_height)),  #Size
                text='>',
                manager=self.ui_manager
            )

        # Yellow Player
        self.yellow_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((80), (385)), #Position
                (200, 200)), #Size
            object_id='#yellow_panel',
            manager=self.ui_manager
        )
        self.image_surface = pygame.image.load('SnakeEyes/Assets/Characters/Profile/mj-profileAlt.png').convert_alpha()

        # Create a UIImage inside the blue panel
        self.image_element = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(  
                (10, 20),  # Image position relative to the blue panel
                (180, 180)),  # Image size (adjust to the size of your image)
            image_surface=self.image_surface,
            manager=self.ui_manager,
            container=self.yellow_panel  # Set the blue panel as the container
        )
        self.yellow_player_index = self.player_type_options.index(Preferences.YELLOW_PLAYER_TYPE)
        self.yellow_player_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((124), (611)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.yellow_player_index],  # Show current option
            manager=self.ui_manager
        )
        

        self.yellow_control_index = self.control_type_options.index(Preferences.YELLOW_CONTROLS)
        self.yellow_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((124), (660)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.yellow_control_index],  # Show current option
            manager=self.ui_manager
        )
        if self.pNum == 3:
            self.yellow_control_left = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((92), (660)), #Position
                    (option_select_width, option_select_height)),  #Size
                text='<',
                manager=self.ui_manager
            )
            self.yellow_control_right = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((236), (660)), #Position
                    (option_select_width, option_select_height)),  #Size
                text='>',
                manager=self.ui_manager
            )

        # Green Player
        self.green_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((1000), (385)), #Position
                (200, 200)), #Size
            object_id='#green_panel',
            manager=self.ui_manager
        )
        self.image_surface = pygame.image.load('SnakeEyes/Assets/Characters/Profile/Jeff Profile Alt1.png').convert_alpha()

        # Create a UIImage inside the blue panel
        self.image_element = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(  
                (10, 20),  # Image position relative to the blue panel
                (180, 180)),  # Image size (adjust to the size of your image)
            image_surface=self.image_surface,
            manager=self.ui_manager,
            container=self.green_panel  # Set the blue panel as the container
        )
        self.green_player_index = self.player_type_options.index(Preferences.GREEN_PLAYER_TYPE)
        self.green_player_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((1044), (611)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.green_player_index],  # Show current option
            manager=self.ui_manager
        )
        
        
        self.green_control_index = self.control_type_options.index(Preferences.GREEN_CONTROLS)
        self.green_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((1044), (660)), #Position
                (player_option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.green_control_index],  # Show current option
            manager=self.ui_manager
        )
        if self.pNum == 4:
            self.green_control_left = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((1012), (660)), #Position
                    (option_select_width, option_select_height)),  #Size
                text='<',
                manager=self.ui_manager
            )
            self.green_control_right = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((1156), (660)), #Position
                    (option_select_width, option_select_height)),  #Size
                text='>',
                manager=self.ui_manager
            )

        ########################
        ##### GAME OPTIONS #####
        ########################

        game_option_y = 304
        game_option_space = 80

        # Finishline
        self.finish_score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((584), (game_option_y + (game_option_space*0))), #Position
                (game_option_label_width, option_label_heigth)),  #Size
            text="$"+str(f'{Preferences.FINISHLINE_SCORE:,}'),  # Show current option
            manager=self.ui_manager
        )
        
        
        # Mods
        
        self.mods_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((584), (game_option_y + (game_option_space*1))), #Position
                (game_option_label_width, option_label_heigth)),  #Size
            text=Preferences.MODS_PREFERENCE,  # Show current option
            manager=self.ui_manager
        )
        
        # Start Button
        

    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")

    ##### Run #####
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.clientProcess()
        self.update()
        self.render()

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
                #print("Importing...")
                self.dataImport(game_state)
                if not self.enabled:
                    self.enableControls()
                #print("Updating...")
                self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
                #self.update()
                #print("Rendering...")
                #self.render()
            except EOFError:
                print("End of ConnectionClient")
                print(self.tempScene)
                self.running = False
                if self.tempScene == 'mgame':
                    #print("Controlls: "+Preferences.BLUE_CONTROLS)
                    self.game.clientInit(self.pNum, self.GC1, self.GC2)
                    self.scene_manager.switch_scene('mgame')
                else:
                    self.scene_manager.switch_scene('menu')
                    self.scene_manager.multiplayer_destroy()

                self.c.close()
                print("Setup EoC Exiting...")

    
    def clientVars(self):
        self.finish_score_label.set_text("$"+str(f'{Preferences.FINISHLINE_SCORE:,}'))
        self.mods_label.set_text(Preferences.MODS_PREFERENCE)

        self.blue_player_label.set_text(Preferences.BLUE_PLAYER_TYPE)
        self.yellow_player_label.set_text(Preferences.YELLOW_PLAYER_TYPE)
        self.green_player_label.set_text(Preferences.GREEN_PLAYER_TYPE)

    ##### Update #####
    def update(self):
        self.clientVars()
        
                    
        if pygame.joystick.get_count() != 0:
            self.control_type_options = [
                "WASD",
                "TFGH",
                "IJKL",
                "Arrows",
                "Controller",
                "None",
            ]
        else:
            self.control_type_options = [
                "WASD",
                "TFGH",
                "IJKL",
                "Arrows",
                "None",
            ]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.c.shutdown(socket.SHUT_WR)
                self.c.close()
                self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')
                # Pause Menu
                if event.key == pygame.K_ESCAPE:
                    #print("Escape")
                    self.scene_manager.switch_scene("pause")

            self.ui_manager.process_events(event) #Update pygame_gui
            if event.type == pygame.USEREVENT:
                # Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    # Player Control Select
                    if self.pNum == 2:
                        if event.ui_element == self.blue_control_left:
                            self.controlSchemeSelect('blue', -1)
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                        if event.ui_element == self.blue_control_right:
                            self.controlSchemeSelect('blue', 1)
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    elif self.pNum == 3:
                        if event.ui_element == self.yellow_control_left:
                            self.controlSchemeSelect('yellow', -1)
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                        if event.ui_element == self.yellow_control_right:
                            self.controlSchemeSelect('yellow', 1)
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    elif self.pNum == 4:
                        if event.ui_element == self.green_control_left:
                            self.controlSchemeSelect('green', -1)
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                        if event.ui_element == self.green_control_right:
                            self.controlSchemeSelect('green', 1)
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

                    # Finishline Score
                    

    

    # Function to handle changing player control scheme
    # Direction: -1: left,   1: right
    #           0: disable, 2: enable
    def controlSchemeSelect(self, color, direction):
        players = {
            "red" : {
                "index" : "red_control_index",
                "label" : self.red_control_label,
                "preference" : "RED_CONTROLS"
            },
            "blue" : {
                "index" : "blue_control_index",
                "label" : self.blue_control_label,
                "preference" : "BLUE_CONTROLS"
            },
            "yellow" : {
                "index" : "yellow_control_index",
                "label" : self.yellow_control_label,
                "preference" : "YELLOW_CONTROLS"
            },
            "green" : {
                "index" : "green_control_index",
                "label" : self.green_control_label,
                "preference" : "GREEN_CONTROLS"
            }
        }
        options = self.control_type_options
        index_attr = players[color]["index"]
        label = players[color]["label"]
        preference_key = players[color]["preference"]
        index = getattr(self, index_attr)  #Get current index

        # If direction is 0, disable control schemes
        if (direction == 0):
            setattr(self, index_attr, (len(options)-1))
            label.set_text("None")
            setattr(Preferences, preference_key, "None")
            return
        # If direction is 2, enable control schemes
        elif (direction == 2):
            setattr(self, index_attr, (len(options)-2))
            index = getattr(self, index_attr)
            direction = 1

        # Do nothing if controls disabled
        if (index == (len(options)-1)):
            return

        # Update Index
        new_index = (index + direction) % (len(options)-1)

        # Handle Overlapping Controls
        tracker = new_index
        while options[new_index] in (Preferences.RED_CONTROLS, Preferences.BLUE_CONTROLS, Preferences.YELLOW_CONTROLS, Preferences.GREEN_CONTROLS):
            # Disabling this for now until multiple controllers can be used
            # if (options[new_index] == "Controller"): #Allows multiple controllers
            #     break
            new_index = (new_index + direction) % (len(options)-1)
            if (new_index == tracker):  #Prevents infinite loops if not enough options
                break
        setattr(self, index_attr, new_index)  #Update index

        # Update Label
        label.set_text(str(options[new_index]))
        # Update Preferences
        setattr(Preferences, preference_key, str(options[new_index]))

    ##### Render #####
    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)

        rect = pygame.Rect(0, 0, 360, 720)
        pygame.draw.rect(self.screen, Settings.COLOR_PRIMARY, rect)
        pygame.draw.line(self.screen, Settings.COLOR_ACCENT, (360, 0), (360, 720), 3)
        pygame.draw.line(self.screen, Settings.COLOR_ACCENT, (0, 360), (360, 360), 3)
        rect = pygame.Rect(920, 0, 360, 720)

        pygame.draw.rect(self.screen, Settings.COLOR_PRIMARY, rect)
        pygame.draw.line(self.screen, Settings.COLOR_ACCENT, (920, 0), (920, 720), 3)
        pygame.draw.line(self.screen, Settings.COLOR_ACCENT, (920, 360), (1280, 360), 3)

        text_y_shift = 5
        

        game_preferences_text = self.HEADER_FONT.get_rect("GAME PREFERENCES")
        game_preferences_text.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, game_preferences_text, "GAME PREFERENCES", Settings.COLOR_TEXT)

        finish_score_rect = self.finish_score_label.get_relative_rect()
        finish_text_rect = self.GAME_FONT.get_rect("FINISHLINE SCORE")
        finish_text_rect.center = (finish_score_rect.centerx, finish_score_rect.top - Settings.FONT_SIZE + text_y_shift)
        self.GAME_FONT.render_to(self.screen, finish_text_rect, "FINISHLINE SCORE", Settings.COLOR_TEXT)
        
        mods_text = "MODIFIERS"
        mods_rect = self.mods_label.get_relative_rect()
        mods_text_rect = self.GAME_FONT.get_rect(mods_text)
        mods_text_rect.center = (mods_rect.centerx, mods_rect.top - Settings.FONT_SIZE + text_y_shift)
        self.GAME_FONT.render_to(self.screen, mods_text_rect, mods_text, Settings.COLOR_TEXT)

        # Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen) 

        pygame.display.flip()


