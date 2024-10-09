#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_tutorial.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest, pygame_gui
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.Scenes.tutorial import Tutorial
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
def setup_tutorial(setup_scene_manager):
    pygame.init()
    tutorial = Tutorial(setup_scene_manager) #Instantiate Tutorial
    tutorial.scene_manager.switch_scene('tutorial') #Set to current scene
    tutorial.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    return tutorial


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
def test_initial_page(setup_tutorial):
    logging.info("Testing Initial Page")
    tutorial = setup_tutorial

    assert(tutorial.tutorial_page_num[tutorial.page_index] == '1/7')


def test_tutorial_pages(setup_tutorial):
    logging.info("Testing Tutorial Pages")
    tutorial = setup_tutorial
    
    #Right button
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '2/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '3/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '4/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '5/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '6/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '7/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '1/7')
    simulate_gui_click(tutorial, tutorial.page_right)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '2/7')

    #Left button
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '1/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '7/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '6/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '5/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '4/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '3/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '2/7')
    simulate_gui_click(tutorial, tutorial.page_left)
    assert(tutorial.tutorial_page_num[tutorial.page_index] == '1/7')


def test_back_button(setup_tutorial):
    logging.info("Testing Back Button")
    tutorial = setup_tutorial

    assert(tutorial.scene_manager.get_scene() == 'tutorial')
    simulate_gui_click(tutorial, tutorial.back_button)
    assert(tutorial.scene_manager.get_scene() == 'menu')