import pygame
try:
    from settings import Settings
except ImportError: #Use absolute file positions when testing
    from SnakeEyes.Code.settings import Settings

class GameStatus:
    def __init__(self, scene_manager, game):
        self.scene_manager = scene_manager
        self.game = game
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
                    self.scene_manager.switch_scene('mods')
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('pause')

    def render(self):
        self.screen.fill((255, 255, 255))
        self.GAME_FONT.render_to(self.screen, (10, 130), "Game Status", (0, 0, 0))
        self.GAME_FONT.render_to(self.screen, (350, 680), "Press SPACE to continue...", (0, 0, 0))
        pCount = 1
        for p in self.game.Players:
            self.GAME_FONT.render_to(self.screen, (10+((pCount-1)*300), 170), "P"+str(pCount)+" Score: "+self.game.getScore(pCount), (0, 0, 0))
            pCount = pCount + 1
            

        pygame.display.flip()