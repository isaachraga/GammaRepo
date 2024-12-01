import pygame
import pygame_gui
from SnakeEyes.Code.settings import Settings

class Credits:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json")
        self.Amari= pygame.image.load('SnakeEyes/Assets/Team/Amari.png')
        self.Dakota= pygame.image.load('SnakeEyes/Assets/Team/Dakota.png')
        self.Zach= pygame.image.load('SnakeEyes/Assets/Team/Zach.png')
        self.Isaac= pygame.image.load('SnakeEyes/Assets/Team/Isaac.png')
        self.Brandon= pygame.image.load('SnakeEyes/Assets/Team/Brandon.png')
        self.Pierce= pygame.image.load('SnakeEyes/Assets/Team/Pierce.png')
        self.David= pygame.image.load('SnakeEyes/Assets/Team/David.png')
        self.Cam= pygame.image.load('SnakeEyes/Assets/Team/Cameron.png')
        self.Nick= pygame.image.load('SnakeEyes/Assets/Team/Nick.png')
        self.Ricky= pygame.image.load('SnakeEyes/Assets/Team/Ricky.png')
        self.nolan= pygame.image.load('SnakeEyes/Assets/Team/Nolan.png')
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
        self.GAME_FONT.render_to(self.screen, (610, 20), "Credits", Settings.COLOR_TEXT)
        self.GAME_FONT.render_to(self.screen, (75, 250),  "Isaac H.   -    Programmer", Settings.COLOR_TEXT)
        self.screen.blit(self.Isaac, (115,90))

        self.GAME_FONT.render_to(self.screen, (375, 250), "Zach A.    -    Programmer", Settings.COLOR_TEXT)   
        self.screen.blit(self.Zach, (415,90))

        self.GAME_FONT.render_to(self.screen, (1000, 250), "Nick N.      -   Artist", Settings.COLOR_TEXT)
        self.screen.blit(self.Nick, (1020,90))

        self.GAME_FONT.render_to(self.screen, (700, 250), "Cameron M.   -   Artist", Settings.COLOR_TEXT)
        self.screen.blit(self.Cam, (720,90))

        self.GAME_FONT.render_to(self.screen, (200, 425),  "Amari O.E.    -     Artist", Settings.COLOR_TEXT)
        self.screen.blit(self.Amari, (240,270))

        self.GAME_FONT.render_to(self.screen, (525, 425), "Dakota D.   -  Music/Sounds", Settings.COLOR_TEXT)
        self.screen.blit(self.Dakota, (565,270))

        self.GAME_FONT.render_to(self.screen, (875, 425), "Brandon R. -  Modifiers", Settings.COLOR_TEXT)
        self.screen.blit(self.Brandon, (895,270))

        self.GAME_FONT.render_to(self.screen, (100, 600), "Nolan Z.", Settings.COLOR_TEXT)
        self.screen.blit(self.nolan, (60,445))

        self.GAME_FONT.render_to(self.screen, (290, 600), "Pierce P.   -  Online multiplayer", Settings.COLOR_TEXT)
        self.screen.blit(self.Pierce, (340,445))

        self.GAME_FONT.render_to(self.screen, (730, 600), "David T.   -  Controller intergration", Settings.COLOR_TEXT)
        self.screen.blit(self.David, (800,445))

        self.GAME_FONT.render_to(self.screen, (1100, 600), "Ricky A.", Settings.COLOR_TEXT)
        self.screen.blit(self.Ricky, (1070,445))

        self.GAME_FONT.render_to(self.screen, (10, 700), "Press S for scene selection", Settings.COLOR_TEXT)

        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()