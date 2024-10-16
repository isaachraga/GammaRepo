#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_inputs.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import pygame, pytest, pygame_gui
import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback

from SnakeEyes.Code.game import Game
from SnakeEyes.Code.scene_manager import SceneManager



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

def test_keyboard_inputs_wasd(setup_game):
    game = setup_game
    logging.info("Testing WASD input")
    #Testing a
    keyboard_input_left(game, pygame.K_a, "WASD")
    #Testing d
    keyboard_input_right(game, pygame.K_d, "WASD")
    #Testing w
    keyboard_input_up(game, pygame.K_w, "WASD")
    #Testing s
    keyboard_input_down(game, pygame.K_s, "WASD")

def test_keyboard_inputs_tfgh(setup_game):
    game = setup_game
    logging.info("Testing TFGH input")
    #Testing a
    keyboard_input_left(game, pygame.K_f, "TFGH")
    #Testing d
    keyboard_input_right(game, pygame.K_h, "TFGH")
    #Testing w
    keyboard_input_up(game, pygame.K_t, "TFGH")
    #Testing s
    keyboard_input_down(game, pygame.K_g, "TFGH")

def test_keyboard_inputs_ijkl(setup_game):
    game = setup_game
    logging.info("Testing IJKL input")
    #Testing a
    keyboard_input_left(game, pygame.K_j, "IJKL")
    #Testing d
    keyboard_input_right(game, pygame.K_l, "IJKL")
    #Testing w
    keyboard_input_up(game, pygame.K_i, "IJKL")
    #Testing s
    keyboard_input_down(game, pygame.K_k, "IJKL")

def test_keyboard_inputs_arrows(setup_game):
    game = setup_game
    logging.info("Testing Arrows input")
    #Testing a
    keyboard_input_left(game, pygame.K_LEFT, "Arrows")
    #Testing d
    keyboard_input_right(game, pygame.K_RIGHT, "Arrows")
    #Testing w
    keyboard_input_up(game, pygame.K_UP, "Arrows")
    #Testing s
    keyboard_input_down(game, pygame.K_DOWN, "Arrows")

    

def keyboard_input_left(game, key, controller):
    
    game.controllerAssignment(game.Players[0], controller)
    location = game.Players[0].position.x
    newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent)  
    game.run() 
    assert(game.Players[0].position.x < location)
    game.playerReset()
    game.playerLocReset()
    
def keyboard_input_right(game, key, controller):
    game.controllerAssignment(game.Players[0], controller)
    location = game.Players[0].position.x
    newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent)  
    game.run() 
    
    assert(game.Players[0].position.x > location)
    game.playerReset()
    game.playerLocReset()

def keyboard_input_up(game, key, controller):
    game.controllerAssignment(game.Players[0], controller)
    location = game.Players[0].position.y
    newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent)  
    game.run() 
    assert(game.Players[0].position.y < location)
    game.playerReset()
    game.playerLocReset()

def keyboard_input_down(game, key, controller):
    game.controllerAssignment(game.Players[0], controller)
    location = game.Players[0].position.y
    newevent = pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.locals.KMOD_NONE)  
    pygame.event.post(newevent)  
    game.run() 
    assert(game.Players[0].position.y > location)
    game.playerReset()
    game.playerLocReset()