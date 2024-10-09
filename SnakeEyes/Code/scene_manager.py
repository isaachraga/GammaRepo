import pygame
from SnakeEyes.Code.game import Game
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code.Scenes.game_status import GameStatus
from SnakeEyes.Code.Scenes.game_mods import GameMods
from SnakeEyes.Code.Scenes.game_win import GameWin
from SnakeEyes.Code.Scenes.pause import Pause
from SnakeEyes.Code.Scenes.scene_selection import SceneSelection
from SnakeEyes.Code.Scenes.options import OptionsMenu
from SnakeEyes.Code.Scenes.main_menu import MainMenu
from SnakeEyes.Code.Scenes.tutorial import Tutorial
from SnakeEyes.Code.Scenes.credits import Credits
from SnakeEyes.Code.Scenes.game_setup import GameSetup




class SceneManager:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        self.scenes = {
            'tutorial': Tutorial(self),
            'options': OptionsMenu(self),
            'menu': MainMenu(self),
            'game': Game(self),
            'credits': Credits(self),
            'scene': SceneSelection(self),
            #'setup': GameSetup(self)
        }
        self.scenes['setup'] = GameSetup(self, self.scenes.get('game'))
        self.scenes['status'] = GameStatus(self, self.scenes.get('game'))
        self.scenes['mods'] = GameMods(self, self.scenes.get('game'))
        self.scenes['pause'] = Pause(self, self.scenes.get('game'))
        self.scenes['win'] = GameWin(self, self.scenes.get('game'))
        
        
        self.current_scene = 'menu'

    def run(self):
        self.running = True
        while self.running:
            scene = self.scenes[self.current_scene]
            scene.run()
        pygame.quit()


    def switch_scene(self, new_scene):
        self.current_scene = new_scene

    def get_scene(self):
        return self.current_scene
    
    def quit(self):
        self.running = False
        

