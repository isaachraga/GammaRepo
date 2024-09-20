import pygame
from settings import Settings

class Credits:
    def __init__(self, screen):
        self.screen = screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (10, 130), "Credits", (0, 0, 0))
        pygame.display.flip()