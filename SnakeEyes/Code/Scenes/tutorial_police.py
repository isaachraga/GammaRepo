import pygame
from settings import Settings

class Police:
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
                if event.key == pygame.K_SPACE:
                    self.scene_manager.switch_scene('tutorial')
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
        self.GAME_FONT.render_to(self.screen, (350, 10), "How To Play 4/4: Police", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 40), "If the police show up, everyone who is still at the mall ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 70), "gets removed and loses everything they have stored in their vault. ", (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 190), "Press SPACE to return to Tutorial", (0, 0, 0))
        
        
        pygame.display.flip()