import pygame
import pygame.freetype
import pygame_gui
from SnakeEyes.Code.settings import Settings

class MainMenu:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.TITLE_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 72)

        self.clock = pygame.time.Clock() #Needed for pygame_gui
        self.load_title_animation("SnakeEyes/Assets/Icons/Title animated.png", 800,300, 30) # Load animated sprite
        self.button_width = 375
        self.button_height = 75

        self.make_GUI()
    ### Load the animated sprite (title animation) ###
    def load_title_animation(self, path, frame_width, frame_height, frame_rate):
        """Loads the animated sprite from a sprite sheet."""
        try:
            self.sprite_sheet = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading sprite sheet: {e}")
            return

        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_rate = frame_rate
        self.frames = self.extract_frames(self.sprite_sheet, frame_width, frame_height)
        self.current_frame_index = 0
        self.frame_counter = 0
        self.total_frames = len(self.frames)

    ### Extract frames from the sprite sheet ###
    def extract_frames(self, sprite_sheet, frame_width, frame_height):
        """Extract frames from the sprite sheet."""
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    ### Update the frame of the animation ###
    def update_title_animation(self):
        """Update the frame of the title animation."""
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.current_frame_index = (self.current_frame_index + 1) % self.total_frames

    ### Draw the current frame of the animation ###
    def draw_title_animation(self):
        current_frame = self.frames[self.current_frame_index]
        self.screen.blit(current_frame, (250, 10))

    def make_GUI(self):
        #Play Game
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), 285), #Position
                (self.button_width, self.button_height)), #Size
            text='Play Game',
            manager=self.ui_manager
        )
        #Tutorial
        self.tutorial_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), 385), #Position
                (self.button_width, self.button_height)), #Size
            text='Tutorial',
            manager=self.ui_manager
        )
        #Options
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), 485), #Position
                (self.button_width, self.button_height)), #Size
            text='Options',
            manager=self.ui_manager
        )
        #Credits
        self.credits_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), 585), #Position
                (self.button_width, self.button_height)), #Size
            text='Credits',
            manager=self.ui_manager
        )
        #Quit
        self.quit_width = 100
        self.quit_height = 75
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH - self.quit_width), (Settings.HEIGHT - self.quit_height)), #Position
                (self.quit_width, self.quit_height)), #Size
            text='QUIT',
            manager=self.ui_manager
        )

    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")
    
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                # Scene Selection

                #self.scene_manager.switch_scene('scene')

   # def render(self):
        #self.screen.fill((255, 255, 255))
        #self.GAME_FONT.render_to(self.screen, (10, 130), "Sticky Fingers", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 395), "Press any key to continue", (0, 0, 0))
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')
            
            self.ui_manager.process_events(event) #Update pygame_gui
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Play Game Button
                    if event.ui_element == self.play_button:
                        self.scene_manager.switch_scene('setup')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    #Tutorial Button
                    if event.ui_element == self.tutorial_button:
                        self.scene_manager.switch_scene('tutorial')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    #Options Button
                    if event.ui_element == self.options_button:
                        self.scene_manager.switch_scene('options')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    #Credits Button
                    if event.ui_element == self.credits_button:
                        self.scene_manager.switch_scene('credits')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    #Quit Button
                    if event.ui_element == self.quit_button:
                        self.scene_manager.quit()
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.screen.fill((0,0,0))
        self.loadingScreen = pygame.image.load('SnakeEyes/Assets/Environment/Background/MainMenuBackground.png')
        self.screen.blit(self.loadingScreen, (-20,45))
        self.update_title_animation()  # Update the animated sprite
        self.draw_title_animation()    # Draw the animated sprit
        
        self.GAME_FONT.render_to(self.screen, (0, 0), "Press S for scene selection (Debug)", Settings.COLOR_TEXT)

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen) 

        pygame.display.flip()