#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, do 'python -m pytest --log-cli-level=INFO'

import pygame
import pytest
import pygame_gui
from unittest.mock import MagicMock  #Import MagicMock for mocking
import os
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
import logging
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.Scenes.game_setup import GameSetup
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code.settings import Settings



########## SETUP ##########
@pytest.fixture
def mock_scene_manager():
    scene_manager = MagicMock()  #Mock the SceneManager
    scene_manager.switch_scene.return_value = "Scene Switch Called" #Mock scene switch function
    return scene_manager

@pytest.fixture
def mock_game():
    game = MagicMock()  #Mock the Game
    return game

@pytest.fixture 
def setup_game_setup(mock_scene_manager, mock_game):
    pygame.init()
    game_setup = GameSetup(mock_scene_manager, mock_game) #Instantiate GameSetup
    game_setup.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    return game_setup


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



########## TESTS ##########

def test_initial_preferences(setup_game_setup):
    logging.info("Testing initial preferences.")
    game_setup = setup_game_setup

    assert Preferences.RED_PLAYER_TYPE == game_setup.player_type_options[game_setup.red_player_index]
    assert Preferences.RED_CONTROLS == game_setup.control_type_options[game_setup.red_control_index]
    assert Preferences.BLUE_PLAYER_TYPE == game_setup.player_type_options[game_setup.blue_player_index]
    assert Preferences.BLUE_CONTROLS == game_setup.control_type_options[game_setup.blue_control_index]
    assert Preferences.YELLOW_PLAYER_TYPE == game_setup.player_type_options[game_setup.yellow_player_index]
    assert Preferences.YELLOW_CONTROLS == game_setup.control_type_options[game_setup.yellow_control_index]
    assert Preferences.GREEN_PLAYER_TYPE == game_setup.player_type_options[game_setup.green_player_index]
    assert Preferences.GREEN_CONTROLS == game_setup.control_type_options[game_setup.green_control_index]

def test_player_selection(setup_game_setup):
    logging.info("Testing player selection.")
    game_setup = setup_game_setup

    # Red Player
    while Preferences.RED_PLAYER_TYPE != 'Player':
        simulate_gui_click(game_setup, game_setup.red_player_right)
    initial_index = game_setup.red_player_index
    simulate_gui_click(game_setup, game_setup.red_player_right)
    assert initial_index != game_setup.red_player_index  # Ensure index has changed
    simulate_gui_click(game_setup, game_setup.red_player_left)
    assert initial_index == game_setup.red_player_index  # Ensure index returned to initial

    # Blue Player
    while Preferences.BLUE_PLAYER_TYPE != 'Player':
        simulate_gui_click(game_setup, game_setup.blue_player_right)
    initial_index = game_setup.blue_player_index
    simulate_gui_click(game_setup, game_setup.blue_player_right)
    assert initial_index != game_setup.blue_player_index  # Ensure index has changed
    simulate_gui_click(game_setup, game_setup.blue_player_left)
    assert initial_index == game_setup.blue_player_index  # Ensure index returned to initial

    # Yellow Player
    while Preferences.YELLOW_PLAYER_TYPE != 'Player':
        simulate_gui_click(game_setup, game_setup.yellow_player_right)
    initial_index = game_setup.yellow_player_index
    simulate_gui_click(game_setup, game_setup.yellow_player_right)
    assert initial_index != game_setup.yellow_player_index  # Ensure index has changed
    simulate_gui_click(game_setup, game_setup.yellow_player_left)
    assert initial_index == game_setup.yellow_player_index  # Ensure index returned to initial

    # Green Player
    while Preferences.GREEN_PLAYER_TYPE != 'Player':
        simulate_gui_click(game_setup, game_setup.green_player_right)
    initial_index = game_setup.green_player_index
    simulate_gui_click(game_setup, game_setup.green_player_right)
    assert initial_index != game_setup.green_player_index  # Ensure index has changed
    simulate_gui_click(game_setup, game_setup.green_player_left)
    assert initial_index == game_setup.green_player_index  # Ensure index returned to initial

def test_control_selection(setup_game_setup):
    logging.info("Testing control selection.")
    game_setup = setup_game_setup

    while Preferences.RED_PLAYER_TYPE != 'Player':
        simulate_gui_click(game_setup, game_setup.red_player_right)
    initial_index = game_setup.red_control_index
    simulate_gui_click(game_setup, game_setup.red_control_right)
    assert initial_index != game_setup.red_control_index
    simulate_gui_click(game_setup, game_setup.red_control_left)
    assert initial_index == game_setup.red_control_index

def test_score_selection(setup_game_setup):
    logging.info("Testing finishline score selection.")
    game_setup = setup_game_setup

    # Increase finish line score
    initial_score = Preferences.FINISHLINE_SCORE
    simulate_gui_click(game_setup, game_setup.finish_score_inc)
    assert Preferences.FINISHLINE_SCORE == initial_score + 10

    # Decrease finish line score
    simulate_gui_click(game_setup, game_setup.finish_score_dec)
    assert Preferences.FINISHLINE_SCORE == initial_score

    # Check score can't go to 0
    while Preferences.FINISHLINE_SCORE > 10:
        simulate_gui_click(game_setup, game_setup.finish_score_dec)
    simulate_gui_click(game_setup, game_setup.finish_score_dec)
    assert Preferences.FINISHLINE_SCORE == 10

    # Restore the initial score
    while Preferences.FINISHLINE_SCORE < initial_score:
        simulate_gui_click(game_setup, game_setup.finish_score_inc)
