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
    logging.info("Testing collider stops movement")
    game = setup_game
    for x in range(40):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 
        #logging.info("Run: "+ str(x)+" | Location: "+ str(game.Players[1].position.y))

    assert(game.Players[1].position.y > 280)
    game.playerReset()
    game.playerLocReset()

def test_collider_stop_movement_and_continue_back(setup_game):
    logging.info("Testing collider stops movement and can continue moving back after")
    game = setup_game
    for x in range(40):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 
        #logging.info("Run: "+ str(x)+" | Location: "+ str(game.Players[1].position.y))

    assert(game.Players[1].position.y > 280)
    location = game.Players[1].position.y

    for x in range(10):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 

    assert(game.Players[1].position.y > location)

    game.playerReset()
    game.playerLocReset()

def test_collider_stop_movement_and_continue_side(setup_game):
    logging.info("Testing collider stops movement and can continue moving to the side after")
    game = setup_game
    for x in range(40):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 
        #logging.info("Run: "+ str(x)+" | Location: "+ str(game.Players[1].position.y))

    assert(game.Players[1].position.y > 280)
    location = game.Players[1].position.x

    for x in range(10):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 

    assert(game.Players[1].position.x < location)

    game.playerReset()
    game.playerLocReset()

def test_car_has_collide(setup_game):
    logging.info("Testing car has collider and stops movement")
    game = setup_game
    for x in range(40):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 
        #logging.info("Run: "+ str(x)+" | Location: "+ str(game.Players[1].position.y))

    assert(game.Players[1].position.y < 493)
    location = game.Players[1].position.x

    for x in range(10):
        newevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f, mod=pygame.locals.KMOD_NONE)  
        pygame.event.post(newevent)  
        game.run() 

    assert(game.Players[1].position.x < location)

    game.playerReset()
    game.playerLocReset()