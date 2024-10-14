#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_pause.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest, pygame_gui
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.Scenes.pause import Pause
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

@pytest.fixture
def setup_game(setup_scene_manager):
    game = setup_scene_manager.scenes['game']
    return game

@pytest.fixture 
def setup_pause_menu(setup_scene_manager, setup_game):
    pygame.init()
    pause_menu = Pause(setup_scene_manager, setup_game) #Instantiate Pause Menu
    pause_menu.scene_manager.switch_scene('pause') #Set to current scene
    pause_menu.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    return pause_menu


#Helper function for simulating GUI clicks
def simulate_gui_click(tested_class, ui_element):
    simulated_event = pygame.event.Event(  #Simulate left click event on pygame_gui button
        pygame.USEREVENT, {
            'user_type': pygame_gui.UI_BUTTON_PRESSED,
            'ui_element': ui_element,
            'mouse_button': 1
        })
    pygame.event.post(simulated_event)
    tested_class.run()  #Allow updates to happen


###############################################
#################### TESTS ####################
###############################################
def test_nav_buttons(setup_pause_menu):
    logging.info("Testing Navigation Buttons")
    pause_menu = setup_pause_menu

    pause_menu.scene_manager.switch_scene('pause')
    assert(pause_menu.scene_manager.get_scene() == 'pause')
    simulate_gui_click(pause_menu, pause_menu.tutorial_button)
    assert(pause_menu.scene_manager.get_scene() == 'tutorial')

    pause_menu.scene_manager.switch_scene('pause')
    assert(pause_menu.scene_manager.get_scene() == 'pause')
    simulate_gui_click(pause_menu, pause_menu.options_button)
    assert(pause_menu.scene_manager.get_scene() == 'options')
    
    pause_menu.scene_manager.switch_scene('pause')
    assert(pause_menu.scene_manager.get_scene() == 'pause')
    simulate_gui_click(pause_menu, pause_menu.credits_button)
    assert(pause_menu.scene_manager.get_scene() == 'credits')
    
    pause_menu.scene_manager.switch_scene('pause')
    assert(pause_menu.scene_manager.get_scene() == 'pause')
    simulate_gui_click(pause_menu, pause_menu.quit_button)
    assert(pause_menu.scene_manager.get_scene() == 'menu')


def test_back(setup_pause_menu):
    logging.info("Testing Back Button")
    pause_menu = setup_pause_menu

    pause_menu.scene_manager.switch_scene('game')
    assert(pause_menu.scene_manager.get_scene() == 'game')
    pause_menu.scene_manager.switch_scene('pause')
    assert(pause_menu.scene_manager.get_scene() == 'pause')
    simulate_gui_click(pause_menu, pause_menu.back_button)
    assert(pause_menu.scene_manager.get_scene() == 'game')
    
    

