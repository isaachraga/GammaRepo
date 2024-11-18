import pygame
import pygame_gui
from SnakeEyes.Code.settings import Settings

class Credits:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json")

        self.clock = pygame.time.Clock() #Needed for pygame_gui
        self.button_width = 150
        self.button_height = 60
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), (Settings.HEIGHT - self.button_height)), #Position
                (self.button_width, self.button_height)), #Size
            text='BACK',
            manager=self.ui_manager
        
        )
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        #self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")
        pass #Does nothing
    
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.scene_manager.quit()

            self.ui_manager.process_events(event)
                    
            if event.type == pygame.KEYDOWN:
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')
            
            if event.type == pygame.USEREVENT:
                # Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Back Button
                    if event.ui_element == self.back_button:
                        self.scene_manager.switch_scene('back')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.ui_manager.update(self.time_delta)
        self.screen.fill(Settings.COLOR_BACKGROUND)
        self.GAME_FONT.render_to(self.screen, (10, 20), "Credits", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (75, 250),  "Issac H.   -    Programmer", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (375, 250), "Zach A.    -    Programmer", Settings.COLOR_TEXT)    
        self.GAME_FONT.render_to(self.screen, (1000, 250), "Nick N.      -   Artist", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (700, 250), "Cameron M.   -   Artist", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (200, 425),  "Amari O.E.    -     Artist", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (525, 425), "Dakota D.   -  Music/Sounds", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (875, 425), "Brandon R. -  Modifiers", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (250, 600), "Pierce P.   -  Online multiplayer", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (750, 600), "David T.   -  Controller intergration", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (10, 700), "Press S for scene selection", Settings.COLOR_TEXT)

        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()