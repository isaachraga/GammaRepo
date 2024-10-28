import pygame
import pygame_gui
import pygame.freetype
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences

class GameStatus:
    def __init__(self, scene_manager, game):
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)

        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.clock = pygame.time.Clock() #Needed for pygame_gui

        self.make_GUI()

    def make_GUI(self):
        self.button_width = 500
        self.button_height = 70

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2)-self.button_width/2, (Settings.HEIGHT)-self.button_height), #Position
                (self.button_width, self.button_height)), #Size
            text='CONTINUE',
            manager=self.ui_manager
        )

        sidePadding = 25
        verticalPadding = 80
        self.back_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((sidePadding), (verticalPadding)), #Position
                (Settings.WIDTH - (sidePadding*2), Settings.HEIGHT - (verticalPadding*2))), #Size
            object_id='#back_panel',
            manager=self.ui_manager
        )
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    
    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            self.ui_manager.process_events(event) #Update pygame_gui

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene_manager.switch_scene('mods')
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.switch_scene('pause')
            
            if event.type == pygame.USEREVENT:
                #Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Continue Button
                    if event.ui_element == self.continue_button:
                        self.scene_manager.switch_scene('mods')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.screen.fill(Settings.COLOR_PRIMARY)

        status_text_rect = self.HEADER_FONT.get_rect("GAME STATUS")
        status_text_rect.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, status_text_rect, "GAME STATUS", Settings.COLOR_TEXT)

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen)    

        #Score
        pCount = len(self.game.Players)

        VerticalPadding = 100
        bufferBetween = 25
        barRight = Settings.WIDTH - 150
        barLeft = 150
        minBarWidth = 10
        barGoalWidth = barRight - (barLeft + minBarWidth)
        totalHeight = Settings.HEIGHT - (VerticalPadding * 2)
        spaceForBars = totalHeight - (bufferBetween * (pCount - 1))
        barHeight = spaceForBars / pCount
        goalBarWidth = 3
        
        #Goal Bar
        goal_rect = pygame.Rect(barRight, VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_TEXT, goal_rect)

        #Intermediate bars
        intermediate_rect = pygame.Rect(barRight - ((barGoalWidth/4)*1), VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, intermediate_rect)
        intermediate_rect = pygame.Rect(barRight - ((barGoalWidth/4)*2), VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, intermediate_rect)
        intermediate_rect = pygame.Rect(barRight - ((barGoalWidth/4)*3), VerticalPadding, goalBarWidth, totalHeight) #x, y, width, height
        pygame.draw.rect(self.screen, Settings.COLOR_ACCENT, intermediate_rect)

        #Player Bars
        pCurIndex = 1
        for p in self.game.Players:
            #Score Bar
            curBarWidth = minBarWidth + (barGoalWidth * (float(self.game.getScore(p.playerNum)) / Preferences.FINISHLINE_SCORE))
            # curBarWidth = minBarWidth + barGoalWidth #DEBUG
            rect = pygame.Rect( barLeft, VerticalPadding+((pCurIndex-1)*(barHeight + bufferBetween)), curBarWidth, barHeight) #x, y, width, height
            pygame.draw.rect(self.screen, p.color, rect)
            
            #Text
            player_num_text = "P"+str(p.playerNum)
            player_num_rect = self.GAME_FONT.get_rect(player_num_text)
            player_num_rect.midright = (rect.left - 5, rect.centery - Settings.FONT_SIZE/2)
            self.GAME_FONT.render_to(self.screen, player_num_rect, player_num_text, Settings.COLOR_TEXT)
            
            player_score_text = self.game.getScore(p.playerNum)
            player_score_rect = self.GAME_FONT.get_rect(player_score_text)
            player_score_rect.midright = (rect.left - 5, rect.centery + Settings.FONT_SIZE/2)
            self.GAME_FONT.render_to(self.screen, player_score_rect, player_score_text, Settings.COLOR_TEXT)

            pCurIndex += 1

        #Goal Text
        goal_text = "Goal"
        goal_text_rect = self.GAME_FONT.get_rect(goal_text)
        goal_text_rect.midleft = (goal_rect.right + 5, goal_rect.centery - Settings.FONT_SIZE/2)
        self.GAME_FONT.render_to(self.screen, goal_text_rect, goal_text, Settings.COLOR_TEXT)

        goal_score_text = str(Preferences.FINISHLINE_SCORE)
        goal_score_rect = self.GAME_FONT.get_rect(goal_score_text)
        goal_score_rect.midleft = (goal_rect.right + 5, goal_rect.centery + Settings.FONT_SIZE/2)
        self.GAME_FONT.render_to(self.screen, goal_score_rect, goal_score_text, Settings.COLOR_TEXT)


        pygame.display.flip()