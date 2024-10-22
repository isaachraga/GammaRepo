import pygame
import pygame_gui
import pygame.freetype
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences

class GameWin:
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
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")

        self.sorted_players = sorted(self.game.Players, key=lambda Player: Player.score, reverse=True)

    
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
                    self.game.statusFlag = False
                    self.scene_manager.switch_scene('menu')
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('pause')
            
            if event.type == pygame.USEREVENT:
                #Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Continue Button
                    if event.ui_element == self.continue_button:
                        self.scene_manager.switch_scene('menu')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")

    def render(self):
        self.screen.fill((255, 255, 255))

        over_text_rect = self.HEADER_FONT.get_rect("GAME OVER")
        over_text_rect.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, over_text_rect, "GAME OVER", (0, 0, 0))

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen)  

        verticalShift = 70
        bottom = Settings.HEIGHT-verticalShift
        spaceBetween = 10
        textPadding = 0.2

        winnerWidth = 375
        winnerHeight = 450
        secondWidth = winnerWidth*(5/6)
        secondHeight = winnerHeight*(5/6)
        thirdWidth = winnerWidth*(2/3)
        thirdHeight = winnerHeight*(2/3)
        fourthWidth = winnerWidth*(2/5)
        fourthHeight = winnerHeight*(2/5)

        pCount = len(self.game.Players)

        #1st place
        if pCount >= 1:
            winner_rect = pygame.Rect((Settings.WIDTH/2)-(winnerWidth/2), (bottom/2)-(winnerHeight/2), #x, y
                            winnerWidth, winnerHeight) #width, height
            pygame.draw.rect(self.screen, (200, 200, 200), winner_rect)

            winner_text = "WANTED"
            currentFontSize = 60
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_wanted_text_rect = currentFont.get_rect(winner_text)
            winner_wanted_text_rect.midtop = (winner_rect.centerx, winner_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_wanted_text_rect, winner_text, (0, 0, 0))
            
            winner_text = f"CRIMINAL MASTERMIND: P{self.sorted_players[0].playerNum}"
            currentFontSize = 23
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_title_text_rect = currentFont.get_rect(winner_text)
            winner_title_text_rect.midtop = (winner_wanted_text_rect.centerx, winner_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_title_text_rect, winner_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[0].character]["profile"])
            image_size = winnerWidth * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (winner_rect.centerx - (image_size/2), winner_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            winner_text = f"${self.sorted_players[0].score:,.2f}"
            currentFontSize = 50
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_score_rect = currentFont.get_rect(winner_text)
            winner_score_rect.midbottom = (winner_rect.centerx, winner_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_score_rect, winner_text, (0, 0, 0))
            
            winner_text = "For the Theft of"
            currentFontSize = 25
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_crime_rect = currentFont.get_rect(winner_text)
            winner_crime_rect.midbottom = (winner_score_rect.centerx, winner_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_crime_rect, winner_text, (0, 0, 0))
        
        #2nd place
        if pCount >= 2:
            second_rect = pygame.Rect(0, 0, secondWidth, secondHeight) #x, y, width, height
            second_rect.bottomright = (winner_rect.left - spaceBetween, winner_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), second_rect)  

            second_text = "WANTED"
            currentFontSize = 50
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_wanted_text_rect = currentFont.get_rect(second_text)
            second_wanted_text_rect.midtop = (second_rect.centerx, second_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_wanted_text_rect, second_text, (0, 0, 0))

            second_text = f"ROBBER: P{self.sorted_players[1].playerNum}"
            currentFontSize = 19
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_title_text_rect = currentFont.get_rect(second_text)
            second_title_text_rect.midtop = (second_wanted_text_rect.centerx, second_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_title_text_rect, second_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[1].character]["profile"])
            image_size = secondWidth * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (second_rect.centerx - (image_size/2), second_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            second_text = f"${self.sorted_players[1].score:,.2f}"
            currentFontSize = 41
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_score_rect = currentFont.get_rect(second_text)
            second_score_rect.midbottom = (second_rect.centerx, second_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_score_rect, second_text, (0, 0, 0))
            
            second_text = "For the Theft of"
            currentFontSize = 20
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_crime_rect = currentFont.get_rect(second_text)
            second_crime_rect.midbottom = (second_score_rect.centerx, second_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_crime_rect, second_text, (0, 0, 0))
        
        #3rd place
        if pCount >= 3:
            third_rect = pygame.Rect(0, 0, thirdWidth, thirdHeight) #x, y, width, height
            third_rect.bottomleft = (winner_rect.right + spaceBetween, winner_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), third_rect)  

            third_text = "WANTED"
            currentFontSize = 40
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_wanted_text_rect = currentFont.get_rect(third_text)
            third_wanted_text_rect.midtop = (third_rect.centerx, third_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_wanted_text_rect, third_text, (0, 0, 0))

            third_text = f"BURGLAR: P{self.sorted_players[2].playerNum}"
            currentFontSize = 15
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_title_text_rect = currentFont.get_rect(third_text)
            third_title_text_rect.midtop = (third_wanted_text_rect.centerx, third_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_title_text_rect, third_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[2].character]["profile"])
            image_size = thirdWidth * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (third_rect.centerx - (image_size/2), third_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            third_text = f"${self.sorted_players[2].score:,.2f}"
            currentFontSize = 33
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_score_rect = currentFont.get_rect(third_text)
            third_score_rect.midbottom = (third_rect.centerx, third_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_score_rect, third_text, (0, 0, 0))
            
            third_text = "For the Theft of"
            currentFontSize = 16
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_crime_rect = currentFont.get_rect(third_text)
            third_crime_rect.midbottom = (third_score_rect.centerx, third_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_crime_rect, third_text, (0, 0, 0))
        
        #4th place
        if pCount >= 4:
            fourth_rect = pygame.Rect(0, 0, fourthWidth, fourthHeight) #x, y, width, height
            fourth_rect.bottomleft = (third_rect.right + spaceBetween, third_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), fourth_rect)  

            fourth_text = "WANTED"
            currentFontSize = 24
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_wanted_text_rect = currentFont.get_rect(fourth_text)
            fourth_wanted_text_rect.midtop = (fourth_rect.centerx, fourth_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_wanted_text_rect, fourth_text, (0, 0, 0))

            fourth_text = f"PETTY THIEF: P{self.sorted_players[3].playerNum}"
            currentFontSize = 9
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_title_text_rect = currentFont.get_rect(fourth_text)
            fourth_title_text_rect.midtop = (fourth_wanted_text_rect.centerx, fourth_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_title_text_rect, fourth_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[3].character]["profile"])
            image_size = fourthWidth * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (fourth_rect.centerx - (image_size/2), fourth_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            fourth_text = f"${self.sorted_players[3].score:,.2f}"
            currentFontSize = 20
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_score_rect = currentFont.get_rect(fourth_text)
            fourth_score_rect.midbottom = (fourth_rect.centerx, fourth_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_score_rect, fourth_text, (0, 0, 0))
            
            fourth_text = "For the Theft of"
            currentFontSize = 10
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_crime_rect = currentFont.get_rect(fourth_text)
            fourth_crime_rect.midbottom = (fourth_score_rect.centerx, fourth_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_crime_rect, fourth_text, (0, 0, 0))


        pygame.display.flip()