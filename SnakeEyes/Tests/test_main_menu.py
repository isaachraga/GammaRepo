#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_main_menu.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest, pygame_gui
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.Scenes.main_menu import MainMenu
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
def setup_main_menu(setup_scene_manager):
    pygame.init()
    main_menu = MainMenu(setup_scene_manager) #Instantiate Main Menu
    main_menu.scene_manager.switch_scene('menu') #Set to current scene
    main_menu.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    return main_menu


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
def test_nav_buttons(setup_main_menu):
    logging.info("Testing Navigation Buttons")
    main_menu = setup_main_menu

    assert(main_menu.scene_manager.get_scene() == 'menu')
    simulate_gui_click(main_menu, main_menu.play_button)
    assert(main_menu.scene_manager.get_scene() == 'setup')

    main_menu.scene_manager.switch_scene('menu')
    assert(main_menu.scene_manager.get_scene() == 'menu')
    simulate_gui_click(main_menu, main_menu.tutorial_button)
    assert(main_menu.scene_manager.get_scene() == 'tutorial')
    
    main_menu.scene_manager.switch_scene('menu')
    assert(main_menu.scene_manager.get_scene() == 'menu')
    simulate_gui_click(main_menu, main_menu.options_button)
    assert(main_menu.scene_manager.get_scene() == 'options')
    
    main_menu.scene_manager.switch_scene('menu')
    assert(main_menu.scene_manager.get_scene() == 'menu')
    simulate_gui_click(main_menu, main_menu.credits_button)
    assert(main_menu.scene_manager.get_scene() == 'credits')

