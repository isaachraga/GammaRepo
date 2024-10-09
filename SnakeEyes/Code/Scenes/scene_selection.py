import pygame
from SnakeEyes.Code.settings import Settings

class SceneSelection:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
    
    def run(self):
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.scene_manager.switch_scene('setup')
                if event.key == pygame.K_2:
                    self.scene_manager.switch_scene('tutorial')
                if event.key == pygame.K_3:
                    self.scene_manager.switch_scene('options')
                if event.key == pygame.K_4:
                    self.scene_manager.switch_scene('credits')  
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.switch_scene('menu')
                    
                

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (10, 70), "Use keyboard to select an option", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 100), "1. Start New Game", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 130), "2. Tutorial", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 160), "3. Options", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 190), "4. Credits", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 220), "ESC. Title Screen", (0, 0, 0))
        pygame.display.flip()