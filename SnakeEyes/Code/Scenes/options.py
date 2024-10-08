import pygame
import pygame.freetype  # Import the freetype module.
import pygame_gui # To install, run: 'python -m pip install pygame_gui==0.6.9'
try:
    from settings import Settings
except ImportError: #Use absolute file positions when testing
    from SnakeEyes.Code.settings import Settings

########## OPTIONS MENU ##########
class OptionsMenu:
    ##### Initial Setup #####
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json")
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)
        self.OPTIONS_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)

        self.menu_width = 500
        self.menu_height = 600
        self.menu_buffer = 10

        self.clock = pygame.time.Clock() #Needed for pygame_gui

        #Buttons
        self.button_width = 150
        self.button_height = 60

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), ((Settings.HEIGHT / 2) + (self.menu_height / 2) - self.button_height - self.menu_buffer)), #Position
                (self.button_width, self.button_height)), #Size
            text='BACK',
            manager=self.ui_manager
        )

        #Sliders
        self.slider_width = 350
        self.slider_height = 20

        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.slider_width / 2)), (400)), #Position
                (self.slider_width, self.slider_height)),  #Size
            start_value=Settings.VOLUME,
            value_range=(0.0, 1.0),
            manager=self.ui_manager
        )

        #Option Selectors
        self.option_select_width = 50
        self.option_select_height = 50
        self.option_label_width = 150
        self.option_label_heigth = 50

        self.fullscreen_options = ["Disabled", "Enabled"]
        self.fullscreen_option_index = 0
        self.fullscreen_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.option_label_width / 2)), (300)), #Position
                (self.option_label_width, self.option_label_heigth)),  #Size
            text=self.fullscreen_options[self.fullscreen_option_index],  # Show current option
            manager=self.ui_manager
        )
        self.fullscreen_left_arrow = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.option_label_width / 2) - (self.option_select_width)), (300)), #Position
                (self.option_select_width, self.option_select_height)),  #Size
            text='<',
            manager=self.ui_manager
        )
        self.fullscreen_right_arrow = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) + (self.option_label_width / 2)), (300)), #Position
                (self.option_select_width, self.option_select_height)),  #Size
            text='>',
            manager=self.ui_manager
        )

    
    ##### Run #####
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0
        self.update()
        self.render()

    ##### Update #####
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
                        self.scene_manager.switch_scene('menu')

                    #Fullscreen Option Select
                    if event.ui_element == self.fullscreen_left_arrow:
                        self.fullscreen_option_index -= 1
                        self.fullscreen_option_index %= len(self.fullscreen_options)  #Wrap list
                        self.fullscreen_label.set_text(self.fullscreen_options[self.fullscreen_option_index])
                        if (self.fullscreen_options[self.fullscreen_option_index] == "Enabled"): #Enable fullscreen
                            self.scene_manager.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT), pygame.FULLSCREEN)
                        else: #Disable fullscreen
                            self.scene_manager.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
                    elif event.ui_element == self.fullscreen_right_arrow:
                        self.fullscreen_option_index += 1
                        self.fullscreen_option_index %= len(self.fullscreen_options)  #Wrap list
                        self.fullscreen_label.set_text(self.fullscreen_options[self.fullscreen_option_index])
                        if (self.fullscreen_options[self.fullscreen_option_index] == "Enabled"): #Enable fullscreen
                            self.scene_manager.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT), pygame.FULLSCREEN)
                        else: #Disable fullscreen
                            self.scene_manager.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
            
                # Check if slider is being used
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    #Volume Slider
                    if event.ui_element == self.volume_slider:
                        Settings.VOLUME = self.volume_slider.get_current_value()
                        print(f"Volume Slider Value: {Settings.VOLUME}")

    ##### Render #####
    def render(self):
        self.ui_manager.update(self.time_delta)

        self.screen.fill((255,255,255))

        rect = pygame.Rect(0, 0, self.menu_width, self.menu_height)
        rect.center = ((Settings.WIDTH / 2), (Settings.HEIGHT / 2))
        pygame.draw.rect(self.screen, (0, 0, 0), rect)
        rect = pygame.Rect(0, 0, self.menu_width-5, self.menu_height-5)
        rect.center = ((Settings.WIDTH / 2), (Settings.HEIGHT / 2))
        pygame.draw.rect(self.screen, (205, 205, 205), rect)

        options_text_rect = self.HEADER_FONT.get_rect("OPTIONS")
        options_text_rect.center = ((Settings.WIDTH / 2), (Settings.HEIGHT / 2) - (self.menu_height / 2) + Settings.HEADER_FONT_SIZE + self.menu_buffer)
        self.HEADER_FONT.render_to(self.screen, options_text_rect, "OPTIONS", (0, 0, 0))

        volume_slider_rect = self.volume_slider.get_relative_rect()
        slider_text_rect = self.OPTIONS_FONT.get_rect("VOLUME")
        slider_text_rect.center = (volume_slider_rect.centerx, volume_slider_rect.top - Settings.FONT_SIZE)
        self.OPTIONS_FONT.render_to(self.screen, slider_text_rect, "VOLUME", (0, 0, 0))

        fullscreen_rect = self.fullscreen_label.get_relative_rect()
        fullscreen_text_rect = self.OPTIONS_FONT.get_rect("FULLSCREEN")
        fullscreen_text_rect.center = (fullscreen_rect.centerx, fullscreen_rect.top - Settings.FONT_SIZE)
        self.OPTIONS_FONT.render_to(self.screen, fullscreen_text_rect, "FULLSCREEN", (0, 0, 0))

        self.OPTIONS_FONT.render_to(self.screen, (0, 0), "Press S for scene selection", (0, 0, 0))


        self.ui_manager.draw_ui(self.screen)

        pygame.display.flip()