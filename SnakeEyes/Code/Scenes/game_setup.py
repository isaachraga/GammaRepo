import pygame
import pygame.freetype
import pygame_gui
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences

########## GAME SETUP MENU ##########
class GameSetup:
    ##### Initial Setup #####
    def __init__(self, scene_manager, game):
        self.game = game
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json")
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)

        self.clock = pygame.time.Clock() #Needed for pygame_gui

        self.makeGUI()

    def makeGUI(self):
        option_select_width = 38
        option_select_height = 38
        option_label_width = 112
        option_label_heigth = 38

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
                (option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.red_player_index],  # Show current option
            manager=self.ui_manager
        )
        self.red_player_left = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((92), (251)), #Position
                (option_select_width, option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.red_player_right = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((236), (251)), #Position
                (option_select_width, option_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )

        self.red_control_index = self.control_type_options.index(Preferences.RED_CONTROLS)
        self.red_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((124), (300)), #Position
                (option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.red_control_index],  # Show current option
            manager=self.ui_manager
        )
        self.red_control_left = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((92), (300)), #Position
                (option_select_width, option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.red_control_right = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((236), (300)), #Position
                (option_select_width, option_select_height)),  #Size
            text='>',
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
                (option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.blue_player_index],  # Show current option
            manager=self.ui_manager
        )
        self.blue_player_left = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((1012), (251)), #Position
                (option_select_width, option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.blue_player_right = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((1156), (251)), #Position
                (option_select_width, option_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )

        self.blue_control_index = self.control_type_options.index(Preferences.BLUE_CONTROLS)
        self.blue_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((1044), (300)), #Position
                (option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.blue_control_index],  # Show current option
            manager=self.ui_manager
        )
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
                (option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.yellow_player_index],  # Show current option
            manager=self.ui_manager
        )
        self.yellow_player_left = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((92), (611)), #Position
                (option_select_width, option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.yellow_player_right = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((236), (611)), #Position
                (option_select_width, option_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )

        self.yellow_control_index = self.control_type_options.index(Preferences.YELLOW_CONTROLS)
        self.yellow_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((124), (660)), #Position
                (option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.yellow_control_index],  # Show current option
            manager=self.ui_manager
        )
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
                (option_label_width, option_label_heigth)),  #Size
            text=self.player_type_options[self.green_player_index],  # Show current option
            manager=self.ui_manager
        )
        self.green_player_left = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((1012), (611)), #Position
                (option_select_width, option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.green_player_right = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((1156), (611)), #Position
                (option_select_width, option_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )

        self.green_control_index = self.control_type_options.index(Preferences.GREEN_CONTROLS)
        self.green_control_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((1044), (660)), #Position
                (option_label_width, option_label_heigth)),  #Size
            text=self.control_type_options[self.green_control_index],  # Show current option
            manager=self.ui_manager
        )
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

        # Finishline Score Select
        self.finish_score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((584), (364)), #Position
                (option_label_width, option_label_heigth)),  #Size
            text=str(f'{Preferences.FINISHLINE_SCORE:,}'),  # Show current option
            manager=self.ui_manager
        )
        self.finish_score_dec = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((552), (364)), #Position
                (option_select_width, option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.finish_score_inc = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((696), (364)), #Position
                (option_select_width, option_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )

        # Start Button
        start_button_width = 150
        start_button_height = 60
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (start_button_width / 2)), (Settings.HEIGHT - start_button_height)), #Position
                (start_button_width, start_button_height)), #Size
            text='START',
            manager=self.ui_manager
        )

    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")

    ##### Run #####
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        self.render()

    ##### Update #####
    def update(self):
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
                self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')

            self.ui_manager.process_events(event) #Update pygame_gui
            if event.type == pygame.USEREVENT:
                # Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Start Button
                    if event.ui_element == self.start_button:
                        self.game.initialization()
                        self.game.delayedInit()
                        self.scene_manager.switch_scene('game')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

                    # Player Type Select
                    if event.ui_element == self.red_player_left:
                        self.playerTypeSelect('red', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.red_player_right:
                        self.playerTypeSelect('red', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.blue_player_left:
                        self.playerTypeSelect('blue', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.blue_player_right:
                        self.playerTypeSelect('blue', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.yellow_player_left:
                        self.playerTypeSelect('yellow', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.yellow_player_right:
                        self.playerTypeSelect('yellow', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.green_player_left:
                        self.playerTypeSelect('green', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.green_player_right:
                        self.playerTypeSelect('green', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

                    # Player Control Select
                    if event.ui_element == self.red_control_left:
                        self.controlSchemeSelect('red', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.red_control_right:
                        self.controlSchemeSelect('red', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.blue_control_left:
                        self.controlSchemeSelect('blue', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.blue_control_right:
                        self.controlSchemeSelect('blue', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.yellow_control_left:
                        self.controlSchemeSelect('yellow', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.yellow_control_right:
                        self.controlSchemeSelect('yellow', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.green_control_left:
                        self.controlSchemeSelect('green', -1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.green_control_right:
                        self.controlSchemeSelect('green', 1)
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

                    # Finishline Score
                    self.score_increments = 50000
                    if event.ui_element == self.finish_score_dec:
                        if (Preferences.FINISHLINE_SCORE > self.score_increments):
                            Preferences.FINISHLINE_SCORE = Preferences.FINISHLINE_SCORE - self.score_increments
                            self.finish_score_label.set_text(str(f'{Preferences.FINISHLINE_SCORE:,}'))
                            self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.finish_score_inc:
                        Preferences.FINISHLINE_SCORE = Preferences.FINISHLINE_SCORE + self.score_increments
                        self.finish_score_label.set_text(str(f'{Preferences.FINISHLINE_SCORE:,}'))
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    # Function to handle changing player type
    def playerTypeSelect(self, color, direction):
        players = {
            "red" : {
                "index" : "red_player_index",
                "label" : self.red_player_label,
                "preference" : "RED_PLAYER_TYPE"
            },
            "blue" : {
                "index" : "blue_player_index",
                "label" : self.blue_player_label,
                "preference" : "BLUE_PLAYER_TYPE"
            },
            "yellow" : {
                "index" : "yellow_player_index",
                "label" : self.yellow_player_label,
                "preference" : "YELLOW_PLAYER_TYPE"
            },
            "green" : {
                "index" : "green_player_index",
                "label" : self.green_player_label,
                "preference" : "GREEN_PLAYER_TYPE"
            }
        }
        options = self.player_type_options
        index_attr = players[color]["index"]
        label = players[color]["label"]
        preference_key = players[color]["preference"]
        # Update Index
        index = getattr(self, index_attr)  #Get current index
        new_index = (index + direction) % len(options)
        setattr(self, index_attr, new_index)  #Update index
        # Update Label
        label.set_text(str(options[new_index]))
        # Update Preferences
        setattr(Preferences, preference_key, str(options[new_index]))

        # Disable control scheme if not a player
        if (options[new_index] != "Player"):
            self.controlSchemeSelect(color, 0)
        # Enable control scheme if player
        else:
            self.controlSchemeSelect(color, 2)

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
        

        game_preferences_text = self.HEADER_FONT.get_rect("GAME PREFERENCES")
        game_preferences_text.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, game_preferences_text, "GAME PREFERENCES", Settings.COLOR_TEXT)

        finish_score_rect = self.finish_score_label.get_relative_rect()
        finish_text_rect = self.GAME_FONT.get_rect("FINISHLINE SCORE")
        finish_text_rect.center = (finish_score_rect.centerx, finish_score_rect.top - Settings.FONT_SIZE)
        self.GAME_FONT.render_to(self.screen, finish_text_rect, "FINISHLINE SCORE", Settings.COLOR_TEXT)

        # Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen) 

        pygame.display.flip()
