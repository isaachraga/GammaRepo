#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_game_win_states.py'
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

def test_game_resets_correctly_on_all_alarms_and_cashout(setup_game):
    game = setup_game
    logging.info("Testing that game resets properly when all alarms are triggered and player continues playing after other player cashes out")
    game.Players[1].status = -1
    assert(game.statusFlag == False)
    game.Stores[0].status = -1
    game.Stores[1].status = -1
    game.Stores[2].status = -1
    game.Stores[3].status = -1
    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()
    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()
    assert(game.statusFlag == False)
    game.Players[1].status = -1
    game.Players[0].status = 1
    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()
    assert(game.statusFlag == False)



def test_game_win_all_cash_out_first_player(setup_game):
    game = setup_game
    logging.info("Testing Game win where all other players cash out, first player cashed out wins")
    game.Players[0].score = 501
    game.Players[0].status = -1
    game.run()
    game.roundCheck()
    assert(game.lastRound is True)
    game.Players[1].status = -1
    game.run()
    game.roundCheck()
    game.Players[2].status = -1
    game.run()
    game.roundCheck()
    game.Players[3].status = -1
    game.run()
    game.roundCheck()

    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()

    assert(game.gameOverFlag is True)
    assert(game.result == "GAME OVER: Player 1 Wins!\nPress Space To Restart")

def test_game_win_all_cash_out_second_player(setup_game):
    game = setup_game
    logging.info("Testing Game win where all other players cash out, second player cashed out wins")
    game.Players[0].score = 501
    game.Players[0].status = -1
    game.run()
    game.roundCheck()
    assert(game.lastRound is True)
    game.Players[1].score = 502
    game.Players[1].status = -1
    game.run()
    game.roundCheck()
    game.Players[2].status = -1
    game.run()
    game.roundCheck()
    game.Players[3].status = -1
    game.run()
    game.roundCheck()

    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()

    assert(game.gameOverFlag is True)
    assert(game.result == "GAME OVER: Player 2 Wins!\nPress Space To Restart")

def test_game_win_all_cash_out_last_player(setup_game):
    game = setup_game
    logging.info("Testing Game win where all other players cash out, last player cashed out wins")
    game.Players[0].score = 501
    game.Players[0].status = -1
    game.run()
    game.roundCheck()
    assert(game.lastRound is True)
    game.Players[1].score = 502
    game.Players[1].status = -1
    game.run()
    game.roundCheck()
    game.Players[2].status = -1
    game.run()
    game.roundCheck()
    game.Players[3].score = 503
    game.Players[3].status = -1
    game.run()
    game.roundCheck()

    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()

    assert(game.gameOverFlag is True)
    assert(game.result == "GAME OVER: Player 4 Wins!\nPress Space To Restart")

def test_game_win_police(setup_game):
    game = setup_game
    logging.info("Testing Game win where police arrive")
    game.Players[0].score = 501
    game.Players[0].status = -1
    game.run()
    game.roundCheck()
    assert(game.lastRound is True)
    game.Players[1].score = 502
    game.Players[1].status = 1
    game.run()
    game.roundCheck()
    game.Players[2].status = 1
    game.run()
    game.roundCheck()
    game.Players[3].status = 1
    game.run()
    game.roundCheck()
    game.policeRoll(game.Stores[0])
    '''
    game.resetTempScores()
    game.police = True
    for s in game.Stores:
        s.status = -1
    game.snakeEyes()
    '''
    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()

    assert(game.gameOverFlag is True)
    assert(game.result == "GAME OVER: Player 1 Wins!\nPress Space To Restart")

def test_game_all_alarms_lower_vault(setup_game):
    game = setup_game
    logging.info("Testing Game win where all alarms are set off and cash-out player wins")
    game.Players[0].score = 501
    game.Players[0].status = -1
    game.run()
    game.roundCheck()
    assert(game.lastRound is True)
    game.Players[1].score = 502
    game.Players[1].status =-1
    game.run()
    game.roundCheck()
    game.Players[2].score = 500
    game.Players[2].status = 1
    game.run()
    game.roundCheck()
    game.Players[3].status = 1
    game.run()
    game.roundCheck()
    
    ### Swap out for space bar posting? ###
    
    for s in game.Stores:
        s.status = -1
    game.alarmedStores = 4
    game.allAlarms = True

    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()
    
    
    assert(game.gameOverFlag is True)
    assert(game.result == "GAME OVER: Player 2 Wins!\nPress Space To Restart")

def test_game_all_alarms_higher_vault_sim_key(setup_game):
    game = setup_game
    logging.info("Testing Game win (simulated key press) all alarms set but player in game has higher vault")
    game.Players[0].score = 501
    game.Players[0].status = -1
    game.run()
    game.roundCheck()
    assert(game.lastRound is True)
    game.Players[1].score = 502
    game.Players[1].status =-1
    game.run()
    game.roundCheck()
    game.Players[2].score = 503
    game.Players[2].status = 1
    game.run()
    game.roundCheck()
    game.Players[3].status = 1
    game.run()
    game.roundCheck()

     
    
    ### Swap out for space bar posting? ###
    
    for s in game.Stores:
        s.status = -1
    game.alarmedStores = 4
    game.allAlarms = True
    newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent) 
    game.run()
    
    
    assert(game.gameOverFlag is True)
    assert(game.result == "GAME OVER: Player 3 Wins!\nPress Space To Restart")
