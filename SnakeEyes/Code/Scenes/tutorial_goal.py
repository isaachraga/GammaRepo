import pygame
from settings import Settings

class Goal:
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
                if event.key == pygame.K_SPACE:
                    self.scene_manager.switch_scene('how')
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('scene')
                

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (350, 10), "Goal", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 40), "The player who passes the goal amount of money the furthest ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 70), "wins. Once a player cashes out past the goal amount, all the ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 100), "other players only have the remainder of that mall to try ", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (10, 130), "and make the most amount of money to win.", (0, 0, 0))

        self.GAME_FONT.render_to(self.screen, (10, 190), "Press SPACE to continue", (0, 0, 0))
        
        
        pygame.display.flip()