#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_options.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest, pygame_gui
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.Scenes.options import OptionsMenu
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
def setup_options_menu(setup_scene_manager):
    pygame.init()
    options_menu = OptionsMenu(setup_scene_manager) #Instantiate Options Menu
    options_menu.scene_manager.switch_scene('options') #Set to current scene
    options_menu.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    return options_menu


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


#Helper function for simulating GUI slider value changes
def simulate_gui_slider(tested_class, ui_element, new_value):
    ui_element.set_current_value(new_value) #Set new value
    simulated_event = pygame.event.Event(   #Create a simulated event for slider change
        pygame.USEREVENT, {
            'user_type': pygame_gui.UI_HORIZONTAL_SLIDER_MOVED,
            'ui_element': ui_element,
            'value': new_value
        })
    pygame.event.post(simulated_event)
    tested_class.run()  #Allow updates to happen



###############################################
#################### TESTS ####################
###############################################
def test_initial_options(setup_options_menu):
    logging.info("Testing Initial Options")
    options_menu = setup_options_menu

    assert Settings.VOLUME == options_menu.volume_slider.get_current_value()
    #assert(options_menu.screen.get_flags() & pygame.FULLSCREEN == 0) #Asserts the game starts with fullscreen disabled


def test_fullscreen(setup_options_menu):
    logging.info("Testing Fullscreen Buttons")
    options_menu = setup_options_menu

    #Set fullscreen to disabled
    if (options_menu.screen.get_flags() & pygame.FULLSCREEN != 0):
        simulate_gui_click(options_menu, options_menu.fullscreen_right_arrow)
    assert(options_menu.screen.get_flags() & pygame.FULLSCREEN == 0) 

    #Test right button
    simulate_gui_click(options_menu, options_menu.fullscreen_right_arrow)
    assert(options_menu.screen.get_flags() & pygame.FULLSCREEN != 0) 
    simulate_gui_click(options_menu, options_menu.fullscreen_right_arrow)
    assert(options_menu.screen.get_flags() & pygame.FULLSCREEN == 0) 
    #Test left button
    simulate_gui_click(options_menu, options_menu.fullscreen_left_arrow)
    assert(options_menu.screen.get_flags() & pygame.FULLSCREEN != 0) 
    simulate_gui_click(options_menu, options_menu.fullscreen_left_arrow)
    assert(options_menu.screen.get_flags() & pygame.FULLSCREEN == 0) 


def test_volume(setup_options_menu):
    logging.info("Testing Volume Slider")
    options_menu = setup_options_menu

    simulate_gui_slider(options_menu, options_menu.volume_slider, 0)
    assert options_menu.volume_slider.get_current_value() == 0
    assert options_menu.volume_slider.get_current_value() == Settings.VOLUME

    simulate_gui_slider(options_menu, options_menu.volume_slider, 0.25)
    assert options_menu.volume_slider.get_current_value() == 0.25
    assert options_menu.volume_slider.get_current_value() == Settings.VOLUME
    
    simulate_gui_slider(options_menu, options_menu.volume_slider, 0.5)
    assert options_menu.volume_slider.get_current_value() == 0.5
    assert options_menu.volume_slider.get_current_value() == Settings.VOLUME
    
    simulate_gui_slider(options_menu, options_menu.volume_slider, 0.75)
    assert options_menu.volume_slider.get_current_value() == 0.75
    assert options_menu.volume_slider.get_current_value() == Settings.VOLUME

    simulate_gui_slider(options_menu, options_menu.volume_slider, 1)
    assert options_menu.volume_slider.get_current_value() == 1
    assert options_menu.volume_slider.get_current_value() == Settings.VOLUME


def test_back(setup_options_menu):
    logging.info("Testing Back Button")
    options_menu = setup_options_menu

    assert(options_menu.scene_manager.get_scene() == 'options')
    simulate_gui_click(options_menu, options_menu.back_button)
    assert(options_menu.scene_manager.get_scene() == 'menu')

