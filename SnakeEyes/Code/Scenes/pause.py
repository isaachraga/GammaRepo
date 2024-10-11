import pygame
from SnakeEyes.Code.settings import Settings

class Pause:
    def __init__(self, scene_manager, game):
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")

    def run(self):
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.scene_manager.switch_scene('tutorial')
                if event.key == pygame.K_2:
                    self.scene_manager.switch_scene('options')
                if event.key == pygame.K_3:
                    self.game.resetGame()
                    self.scene_manager.switch_scene('menu')
                if event.key == pygame.K_4:
                    self.scene_manager.switch_scene('game')
                if event.key == pygame.K_5:
                    self.scene_manager.switch_scene('credits')
                

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (10, 70), "Tap a number key to change the scene", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 100), "1. Tutorial", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 130), "2. Options", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 160), "3. Quit Game", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 190), "4. Return to game", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 220), "5. Credits", (0, 0, 0))
        pygame.display.flip()