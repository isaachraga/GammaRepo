import pygame
import pygame_gui
from SnakeEyes.Code.settings import Settings

class Pause:
    def __init__(self, scene_manager, game):
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json")

        self.menu_width = 500
        self.menu_height = 600
        self.menu_buffer = 10

        self.clock = pygame.time.Clock() #Needed for pygame_gui

        #Buttons
        self.button_width = 300
        self.button_height = 70
        self.button_stagger = 80
        self.button_y = 150

        self.tutorial_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), (self.button_y + self.button_stagger*0)), #Position
                (self.button_width, self.button_height)), #Size
            text='TUTORIAL',
            manager=self.ui_manager
        )
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), (self.button_y + self.button_stagger*1)), #Position
                (self.button_width, self.button_height)), #Size
            text='OPTIONS',
            manager=self.ui_manager
        )
        self.credits_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), (self.button_y + self.button_stagger*2)), #Position
                (self.button_width, self.button_height)), #Size
            text='CREDITS',
            manager=self.ui_manager
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), (self.button_y + self.button_stagger*3.5)), #Position
                (self.button_width, self.button_height)), #Size
            text='QUIT GAME',
            manager=self.ui_manager
        )

        self.back_width = 150
        self.back_height = 60
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.back_width / 2)), ((Settings.HEIGHT / 2) + (self.menu_height / 2) - self.back_height - self.menu_buffer)), #Position
                (self.back_width, self.back_height)), #Size
            text='BACK',
            manager=self.ui_manager
        )
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        # self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")
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
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.switch_scene("back")

            if event.type == pygame.USEREVENT:
                # Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.tutorial_button:
                        self.scene_manager.switch_scene('tutorial')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.options_button:
                        self.scene_manager.switch_scene('options')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.credits_button:
                        self.scene_manager.switch_scene('credits')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.quit_button:
                        self.game.resetGame()
                        self.scene_manager.switch_scene('menu')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    if event.ui_element == self.back_button:
                        self.scene_manager.switch_scene('back')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                

    def render(self):
        self.ui_manager.update(self.time_delta)
        self.screen.fill(Settings.COLOR_BACKGROUND)

        rect = pygame.Rect(0, 0, self.menu_width, self.menu_height)
        rect.center = ((Settings.WIDTH / 2), (Settings.HEIGHT / 2))
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, rect)
        rect = pygame.Rect(0, 0, self.menu_width-5, self.menu_height-5)
        rect.center = ((Settings.WIDTH / 2), (Settings.HEIGHT / 2))
        pygame.draw.rect(self.screen, Settings.COLOR_PRIMARY, rect)

        options_text_rect = self.HEADER_FONT.get_rect("PAUSED")
        options_text_rect.center = ((Settings.WIDTH / 2), (Settings.HEIGHT / 2) - (self.menu_height / 2) + Settings.HEADER_FONT_SIZE + self.menu_buffer)
        self.HEADER_FONT.render_to(self.screen, options_text_rect, "PAUSED", Settings.COLOR_TEXT)
        
        self.ui_manager.draw_ui(self.screen)

        pygame.display.flip()