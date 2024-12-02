import pygame
from SnakeEyes.Code.game import Game
from SnakeEyes.Code.gameHOST import GameHOST
from SnakeEyes.Code.gameCLIENT import GameCLIENT
from SnakeEyes.Code.settings import Settings
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code.Scenes.multiplayer_setup import MultiplayerSetup
from SnakeEyes.Code.Scenes.game_setupSERV import GameSetupSERV
from SnakeEyes.Code.Scenes.game_setupCLIENT import GameSetupCLIENT
from SnakeEyes.Code.Scenes.game_status import GameStatus
from SnakeEyes.Code.Scenes.game_statusSERV import GameStatusSERV
from SnakeEyes.Code.Scenes.game_statusCLIENT import GameStatusCLIENT
from SnakeEyes.Code.Scenes.game_mods import GameMods
from SnakeEyes.Code.Scenes.game_modsSERV import GameModsSERV
from SnakeEyes.Code.Scenes.game_modsCLIENT import GameModsCLIENT
from SnakeEyes.Code.Scenes.game_win import GameWin
from SnakeEyes.Code.Scenes.game_winSERV import GameWinSERV
from SnakeEyes.Code.Scenes.game_winCLIENT import GameWinCLIENT
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
            'mSetup': MultiplayerSetup(self),
        }
        
        self.scenes['setup']  = GameSetup(self,  self.scenes.get('game'))
        self.scenes['status'] = GameStatus(self, self.scenes.get('game'), False)
        self.scenes['mods']   = GameMods(self,   self.scenes.get('game'), False)
        self.scenes['pause']  = Pause(self,      self.scenes.get('game'), False)
        self.scenes['win']    = GameWin(self,    self.scenes.get('game'), False)
        #Scenes that are "nested" in other scenes. Can be nested repeatedly
        #Have the ability to go back to previous scene with switch_scene('back')
        self.nested_scenes = ['tutorial', 'options', 'scene', 'pause', 'credits']
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
    
    def multiplayer_init(self, host):
        if host:
            self.scenes['mgame']  = GameHOST(self)
            self.scenes['msetup2']  = GameSetupSERV(self,  self.scenes.get('mgame'))
            self.scenes['mstatus'] = GameStatusSERV(self, self.scenes.get('mgame'), True)
            self.scenes['mmods']   = GameModsSERV(self,   self.scenes.get('mgame'), True)
            self.scenes['mwin']    = GameWinSERV(self,    self.scenes.get('mgame'), True)
        else:
            self.scenes['mgame']  = GameCLIENT(self)
            self.scenes['msetup2']  = GameSetupCLIENT(self,  self.scenes.get('mgame'))
            self.scenes['mstatus'] = GameStatusCLIENT(self, self.scenes.get('mgame'), True)
            self.scenes['mmods']   = GameModsCLIENT(self,   self.scenes.get('mgame'), True)
            self.scenes['mwin']    = GameWinCLIENT(self,    self.scenes.get('mgame'), True)
        
        self.scenes['mpause']  = Pause(self,      self.scenes.get('mgame'), True)
        
    
    def multiplayer_destroy(self):
        Preferences.FINISHLINE_SCORE = 1000000
        Preferences.MODS_PREFERENCE = "Enabled"

        #Player types: Player, CPU, or None
        Preferences.RED_PLAYER_TYPE = "Player"
        Preferences.BLUE_PLAYER_TYPE = "CPU"
        Preferences.YELLOW_PLAYER_TYPE = "None"
        Preferences.GREEN_PLAYER_TYPE = "None"

        #Player control schemes
        Preferences.RED_CONTROLS = "WASD"
        Preferences.BLUE_CONTROLS = "None"
        Preferences.YELLOW_CONTROLS = "None"
        Preferences.GREEN_CONTROLS = "None"

        del self.scenes["mgame"]
        del self.scenes["msetup2"]
        del self.scenes["mstatus"]
        del self.scenes["mmods"]
        del self.scenes["mpause"]
        del self.scenes["mwin"]


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