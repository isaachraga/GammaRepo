import pygame
import pygame.freetype
import pygame_gui
from SnakeEyes.Code.settings import Settings

class MultiplayerSetup:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.GAME_FONT2 = pygame.font.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.TITLE_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 72)

        self.clock = pygame.time.Clock() #Needed for pygame_gui
        self.button_width = 375
        self.button_height = 75

        self.GC1 = ''
        self.GC2 = ''

        self.make_GUI()
    ### Load the animated sprite (title animation) ###

    

    def make_GUI(self):
        #Create Game
        self.create_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), 285), #Position
                (self.button_width, self.button_height)), #Size
            text='Create Game',
            manager=self.ui_manager
        )
        #Join Game
        self.join_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((Settings.WIDTH / 2) - (self.button_width / 2)), 385), #Position
                (self.button_width, self.button_height)), #Size
            text='Join Game',
            manager=self.ui_manager
            )
        
        #Game Code Enter
        self.input_rect_1 = pygame.Rect(((Settings.WIDTH / 2) - (self.button_width / 2))+50, 535, 32, 50) 
        self.input_rect_2 = pygame.Rect(((Settings.WIDTH / 2) - (self.button_width / 2))+150, 535, 140, 50) 
        self.active1 = False
        self.active2 = False

        #Back
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

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if self.input_rect_1.collidepoint(event.pos): 
                    self.active1 = True
                else: 
                    self.active1 = False
                
                if self.input_rect_2.collidepoint(event.pos): 
                    self.active2 = True
                else: 
                    self.active2 = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: 
  
                # get text input from 0 to -1 i.e. end. 
                    if self.active1:
                        self.GC1 = self.GC1[:-1] 
                    elif self.active2:
                        self.GC2 = self.GC2[:-1] 
            # Unicode standard is used for string 
            # formation 
                elif self.active1 and len(self.GC1) < 1:
                    self.GC1 += event.unicode
                    #print(str(len(self.GC1))+self.GC1)
                elif self.active2 and len(self.GC2) < 5:
                    self.GC2 += event.unicode
                    #print(str(len(self.GC2))+self.GC2)

                     
                # Scene Selection

                #self.scene_manager.switch_scene('scene')

   # def render(self):
        #self.screen.fill((255, 255, 255))
        #self.GAME_FONT.render_to(self.screen, (10, 130), "Sticky Fingers", (0, 0, 0))
        #self.GAME_FONT.render_to(self.screen, (10, 395), "Press any key to continue", (0, 0, 0))
                if event.key == pygame.K_s and not (self.active1 or self.active2):
                    self.scene_manager.switch_scene('scene')
            
            self.ui_manager.process_events(event) #Update pygame_gui
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Play Game Button
                    if event.ui_element == self.create_button:
                        self.scene_manager.multiplayer_init(True)
                        self.scene_manager.scenes["msetup2"].ServerSetup()
                        self.scene_manager.switch_scene('msetup2')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    #Tutorial Button
                    if event.ui_element == self.join_button and (len(self.GC1) == 1 and len(self.GC2) == 5):
                        self.scene_manager.multiplayer_init(False)
                        self.scene_manager.scenes["msetup2"].ClientSetup(self.GC1, self.GC2)
                        self.scene_manager.switch_scene('msetup2')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                    #Quit Button
                    if event.ui_element == self.quit_button:
                        self.scene_manager.quit()
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.screen.fill((0,0,0))
        self.loadingScreen = pygame.image.load('SnakeEyes/Assets/Environment/Background/MainMenuBackground.png')
        self.screen.blit(self.loadingScreen, (-20,45))
        
        # self.GAME_FONT.render_to(self.screen, (0, 0), "Press S for scene selection (Debug)", Settings.COLOR_TEXT)

        if len(self.GC1) != 1 or len(self.GC2) != 5:
            self.GAME_FONT.render_to(self.screen, (((Settings.WIDTH / 2) - (self.button_width / 2))+50, 485), "Enter Game Code to Join Game", (255,255,255))

        pygame.draw.rect(self.screen, (255,255,255), self.input_rect_1)
        pygame.draw.rect(self.screen, (255,255,255), self.input_rect_2)  
  
        text_surface1 = self.GAME_FONT2.render(self.GC1, True, (0,0,0)) 
        text_surface2 = self.GAME_FONT2.render(self.GC2, True, (0,0,0))
        # render at position stated in arguments 
        self.screen.blit(text_surface1, (self.input_rect_1.x+5, self.input_rect_1.y+5)) 
        self.screen.blit(text_surface2, (self.input_rect_2.x+5, self.input_rect_2.y+5))

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen) 

        pygame.display.flip()