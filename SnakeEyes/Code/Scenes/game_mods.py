import pygame
from SnakeEyes.Code.settings import Settings

class GameMods:
    def __init__(self, scene_manager, game):
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")
    
    def run(self):
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.statusFlag = False
                    self.scene_manager.switch_scene('game')
                # Scene Selection
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.switch_scene('pause')

    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)
        self.GAME_FONT.render_to(self.screen, (10, 130), "Game Mods", Settings.COLOR_TEXT)
        
        self.GAME_FONT.render_to(self.screen, (350, 680), "Press SPACE to continue...", Settings.COLOR_TEXT)
        pygame.display.flip()