import pygame
from settings import Settings
from coreV2 import Game
from Scenes.scene_selection import SceneSelection
from Scenes.options import OptionsMenu
from Scenes.main_menu import MainMenu
from Scenes.tutorial import Tutorial
from Scenes.credits import Credits

class SceneManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        self.scenes = {
            'tutorial': Tutorial(self),
            'options': OptionsMenu(self),
            'menu': MainMenu(self),
            'game': Game(self),
            'credits': Credits(self),
            'scene': SceneSelection(self)
        }
        self.current_scene = 'game'

    def run(self):
        self.running = True
        while self.running:
            scene = self.scenes[self.current_scene]
            scene.run()
        pygame.quit()


    def switch_scene(self, new_scene):
        self.current_scene = new_scene

    def get_scene(self):
        return self.scenes[self.current_scene]
    
    def quit(self):
        self.running = False
        

