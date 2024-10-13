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
        self.current_music = ""
        self.scenes = {
            'tutorial': Tutorial(self),
            'options':  OptionsMenu(self),
            'menu':     MainMenu(self),
            'game':     Game(self),
            'credits':  Credits(self),
            'scene':    SceneSelection(self),
        }
        self.scenes['setup']  = GameSetup(self,  self.scenes.get('game'))
        self.scenes['status'] = GameStatus(self, self.scenes.get('game'))
        self.scenes['mods']   = GameMods(self,   self.scenes.get('game'))
        self.scenes['pause']  = Pause(self,      self.scenes.get('game'))
        self.scenes['win']    = GameWin(self,    self.scenes.get('game'))

        #Scenes that are "nested" in other scenes. Can be nested repeatedly
        #Have the ability to go back to previous scene with switch_scene('back')
        self.nested_scenes = ['tutorial', 'options', 'scene', 'pause']
        self.nested_stack = []
        
        self.switch_scene('menu')

    ### GAME ENGINE ###
    def run(self):
        self.running = True
        while self.running:
            scene = self.scenes[self.current_scene]
            scene.run()
        pygame.quit()

    def quit(self):
        self.running = False


    ### SCENE MANAGEMENT ###
    def switch_scene(self, new_scene):
        #Returning from a nested scene
        if new_scene == "back":
            self.current_scene = self.nested_stack.pop()
        else:
            #Adding a new nested scene
            if new_scene in self.nested_scenes:
                self.nested_stack.append(self.current_scene)
            #Clear nested scenes if switching to a non-nested scene
            elif len(self.nested_stack) != 0:
                self.nested_stack.clear()
            #Switch Current Scene
            self.current_scene = new_scene
        #Invoke on-enter function
        self.scenes[self.current_scene].on_scene_enter()

    def get_scene(self):
        return self.current_scene    


    ### SOUND MANAGEMENT ###
    # Sound Effects #
    def play_sound(self, sound_path):
        sound_effect = pygame.mixer.Sound(sound_path)
        sound_effect.set_volume(Settings.SFX_VOLUME)
        sound_effect.play()
    
    # Music #   
    def play_music(self, music_path):
        if self.current_music != music_path: #If the new song is different from the current one
            pygame.mixer.music.stop() #Stop any previous music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(Settings.BGM_VOLUME)
            pygame.mixer.music.play(-1)  #-1 makes it loop
            self.current_music = music_path
    
    def update_volume(self):
        pygame.mixer.music.set_volume(Settings.BGM_VOLUME)

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = ""