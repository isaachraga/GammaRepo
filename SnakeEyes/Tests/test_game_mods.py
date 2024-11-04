#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_game_mods.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.game import Game
from SnakeEyes.Code.scene_manager import SceneManager
from SnakeEyes.Code.preferences import Preferences
from SnakeEyes.Code import modifier



###############################################
#################### SETUP ####################
###############################################
@pytest.fixture
def setup_scene_manager():
    pygame.init()
    scene_manager = SceneManager()
    return scene_manager

@pytest.fixture
def setup_preferences():
    Preferences.RED_PLAYER_TYPE = "Player"
    Preferences.BLUE_PLAYER_TYPE = "Player"
    Preferences.YELLOW_PLAYER_TYPE = "Player"
    Preferences.GREEN_PLAYER_TYPE = "Player"

    Preferences.RED_CONTROLS = "WASD"
    Preferences.BLUE_CONTROLS = "TFGH"
    Preferences.YELLOW_CONTROLS = "IJKL"
    Preferences.GREEN_CONTROLS = "Arrows"
    return True

@pytest.fixture 
def setup_game(setup_scene_manager, setup_preferences):

    pygame.init()
    game = Game(setup_scene_manager) #Instantiate Game
    #Set to current scene
    pref = setup_preferences
    if pref:
        game.initialization()
        game.delayedInit()
        game.scene_manager.switch_scene('game')
        game.testing = True
        game.run()

    return game




###############################################
#################### TESTS ####################
###############################################
def test_lucky_streak(setup_game):
    logging.info("Testing that lucky streak is working properly")
    game = setup_game
    game.Players[0].currentMods[modifier.lucky_streak]=modifier.lucky_streak
    game.Stores[0].players.append(game.Players[0])
    game.Stores[0].players.append(game.Players[1])
    game.Players[0].streak = 1
    game.defaultRoll(game.Stores[0])
    assert(game.Players[0].tmpScore == round(game.Players[0].tmpScore*1.05, 2))

def test_lucky_streak_removal(setup_game):
    game = setup_game
    logging.info("Testing that lucky streak gets removed")
    game.Players[0].currentMods[modifier.lucky_streak]=modifier.lucky_streak
    game.Stores[0].players.append(game.Players[0])
    game.alarmedStoreRoll(game.Stores[0])
    assert(len(game.Players[0].currentMods) == 0)

def test_paid_off(setup_game):
    logging.info("Testing that paid off is working properly")
    game = setup_game
    game.Players[0].currentMods[modifier.paid_off]=modifier.paid_off
    game.Stores[0].players.append(game.Players[0])
    game.Stores[0].players.append(game.Players[1])
    game.Players[0].score = 100
    game.Players[1].score = 200
    game.policeRoll(game.Stores[0])
    assert(game.Players[0].score == 100)
    assert(game.Players[1].score == 0)

def test_paid_off_removal(setup_game):
    game = setup_game
    logging.info("Testing that paid off gets removed")
    game.Players[0].currentMods[modifier.paid_off]=modifier.paid_off
    game.Stores[0].players.append(game.Players[0])
    game.policeRoll(game.Stores[0])
    assert(len(game.Players[0].currentMods) == 0)

def test_quick_hands(setup_game):
    logging.info("Testing that paid off is working properly")
    game = setup_game
    game.Players[0].currentMods[modifier.quick_hands]=modifier.quick_hands
    game.Stores[0].players.append(game.Players[0])
    game.Stores[0].players.append(game.Players[1])
    game.Players[0].tmpScore = 100
    game.Players[1].tmpScore = 200
    game.alarmedStoreRoll(game.Stores[0])
    assert(game.Players[0].tmpScore == 100)
    assert(game.Players[1].tmpScore == 0)

def test_quick_hands_removal(setup_game):
    game = setup_game
    logging.info("Testing that paid off gets removed")
    game.Players[0].currentMods[modifier.quick_hands]=modifier.quick_hands
    game.Stores[0].players.append(game.Players[0])
    game.alarmedStoreRoll(game.Stores[0])
    assert(len(game.Players[0].currentMods) == 0)




