#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_game_collider.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.game import Game
from SnakeEyes.Code.scene_manager import SceneManager
from SnakeEyes.Code.preferences import Preferences



###############################################
#################### SETUP ####################
###############################################
@pytest.fixture
def setup_scene_manager():
    pygame.init()
    scene_manager = SceneManager()
    return scene_manager

@pytest.fixture 
def setup_game(setup_scene_manager):

    pygame.init()
    game = Game(setup_scene_manager) #Instantiate Game
     #Set to current scene
    game.initialization()
    game.delayedInit()
    game.scene_manager.switch_scene('game')
    game.testing = True
    game.run()
    return game




###############################################
#################### TESTS ####################
###############################################


def test_collider_stop_movement(setup_game):
    game = setup_game