import pygame
import pytest
from unittest.mock import MagicMock  #Import MagicMock for mocking

from SnakeEyes.Code.Scenes.game_setup import GameSetup
from SnakeEyes.Code.preferences import Preferences

@pytest.fixture
def mock_scene_manager():
    mock_scene_manager = MagicMock()  #Mock the SceneManager
    mock_scene_manager.switch_scene.return_value = "Scene Switch Called" #Mock scene switch function
    return mock_scene_manager

@pytest.fixture
def mock_game():
    mock_game = MagicMock()  #Mock the Game
    return mock_game

@pytest.fixture 
def setup_game_setup(mock_scene_manager):
    pygame.init()
    game_setup = GameSetup(mock_scene_manager, mock_game) #Instantiate GameSetup
    return game_setup

def test_initial_preferences(setup_game_setup):
    game_setup = setup_game_setup

    assert Preferences.RED_PLAYER_TYPE == game_setup.player_type_options[game_setup.red_player_index]
    assert Preferences.RED_CONTROLS == game_setup.control_type_options[game_setup.red_control_index]
    assert Preferences.BLUE_PLAYER_TYPE == game_setup.player_type_options[game_setup.blue_player_index]
    assert Preferences.BLUE_CONTROLS == game_setup.control_type_options[game_setup.blue_control_index]
    assert Preferences.YELLOW_PLAYER_TYPE == game_setup.player_type_options[game_setup.yellow_player_index]
    assert Preferences.YELLOW_CONTROLS == game_setup.control_type_options[game_setup.yellow_control_index]
    assert Preferences.GREEN_PLAYER_TYPE == game_setup.player_type_options[game_setup.green_player_index]
    assert Preferences.GREEN_CONTROLS == game_setup.control_type_options[game_setup.green_control_index]
