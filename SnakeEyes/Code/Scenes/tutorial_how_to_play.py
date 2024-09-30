import pygame
from settings import Settings

class HowToPlay:
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
                    self.scene_manager.switch_scene('money')
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
        self.GAME_FONT.render_to(self.screen, (350, 10), "How To Play 1/4: Gameplay", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 40), "All players will start in a mall and walk around to find ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 70), "stores with desirable risk and rewards. Once all players ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 100), "have either selected a store to rob or cashed out their ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 130), "cash-on-hand, the players will initiate their robbery ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 160), "and find out how much they grabbed, if they set off an ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 190), "alarm, or if the police arrived.", (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 250), "Press SPACE to continue", (0, 0, 0))
        
        
        pygame.display.flip()