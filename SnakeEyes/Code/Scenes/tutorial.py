import pygame
from settings import Settings

class Tutorial:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.controlSchemeNum = 0
    
    def run(self):
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.controlSchemeNum == 0:
                        self.controlSchemeNum = 4
                    else:
                        self.controlSchemeNum = self.controlSchemeNum - 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.controlSchemeNum == 4:
                        self.controlSchemeNum = 0
                    else:
                        self.controlSchemeNum = self.controlSchemeNum + 1

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (350, 10), "Tutorial", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 30), "Sticky Fingers description", (0, 0, 0))
        self.controlStart = 500
        self.GAME_FONT.render_to(self.screen, (10, self.controlStart), "Control Schemes: (press a/s or right/left to scroll)", (0, 0, 0))
        match self.controlSchemeNum:
            case 0:
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+40), "---Keyboard 1---", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+70), "Movement:  Up - W  |  Down - S  |  Left - A  |  Right - D", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+100), "Interaction:  Select - 1  |  Cash Out - 2  |  Pause/Menu - SHIFT+S", (0, 0, 0))
            case 1:
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+40), "---Keyboard 2---", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+70), "Movement:  Up - T  |  Down - G  |  Left - F  |  Right - H", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+100), "Interaction:  Select - 3  |  Cash Out - 4  |  Pause/Menu - SHIFT+S", (0, 0, 0))
            case 2:
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+40), "---Keyboard 3---", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+70), "Movement:  Up - I  |  Down - K  |  Left - J  |  Right - L", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+100), "Interaction:  Select - 5  |  Cash Out - 6  |  Pause/Menu - SHIFT+S", (0, 0, 0))
            case 3:
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+40), "---Keyboard 4---", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+70), "Movement:  Arrow Keys", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+100), "Interaction:  Select - 7  |  Cash Out - 8  |  Pause/Menu - SHIFT+S", (0, 0, 0))
            case 4:
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+40), "---Controller---", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+70), "Movement:  Right Joystick or D-pad", (0, 0, 0))
                self.GAME_FONT.render_to(self.screen, (10, self.controlStart+100), "Interaction:  Select - South Button  |  Cash Out - East Button  |  Pause/Menu - Start Button", (0, 0, 0))

        pygame.display.flip()