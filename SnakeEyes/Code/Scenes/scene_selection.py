import pygame
from settings import Settings

class SceneSelection:
    def __init__(self, screen):
        self.screen = screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (10, 70), "Hold shift and tap a number key to change the scene", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 100), "1. Tutorial", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 130), "2. Options", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 160), "3. Main Menu", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 190), "4. Return to game", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 220), "5. Credits", (0, 0, 0))
        pygame.display.flip()