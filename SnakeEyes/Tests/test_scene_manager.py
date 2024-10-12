#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_scene_manager.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.scene_manager import SceneManager
from SnakeEyes.Code.settings import Settings


###############################################
#################### SETUP ####################
###############################################
@pytest.fixture
def setup_scene_manager():
    pygame.init()
    scene_manager = SceneManager()
    return scene_manager

###############################################
#################### TESTS ####################
###############################################
def test_scene_switch(setup_scene_manager):
    logging.info("Testing Scene Switching")
    scene_manager = setup_scene_manager

    scene_manager.switch_scene('tutorial')
    assert(scene_manager.get_scene() == 'tutorial')
    scene_manager.switch_scene('options')
    assert(scene_manager.get_scene() == 'options')
    scene_manager.switch_scene('menu')
    assert(scene_manager.get_scene() == 'menu')
    scene_manager.switch_scene('game')
    assert(scene_manager.get_scene() == 'game')
    scene_manager.switch_scene('credits')
    assert(scene_manager.get_scene() == 'credits')
    scene_manager.switch_scene('scene')
    assert(scene_manager.get_scene() == 'scene')
    scene_manager.switch_scene('setup')
    assert(scene_manager.get_scene() == 'setup')
    scene_manager.switch_scene('status')
    assert(scene_manager.get_scene() == 'status')
    scene_manager.switch_scene('mods')
    assert(scene_manager.get_scene() == 'mods')
    scene_manager.switch_scene('pause')
    assert(scene_manager.get_scene() == 'pause')
    scene_manager.switch_scene('win')
    assert(scene_manager.get_scene() == 'win')