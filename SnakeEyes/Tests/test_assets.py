#For pytest, file must start with 'test_'
#For pytest, function must start with 'test_'
#To run manually, run 'python -m pytest SnakeEyes/Tests/test_assets.py'
#To run all tests, run 'python -m pytest SnakeEyes/Tests'

import os, logging
os.environ["SDL_VIDEODRIVER"] = "dummy" #Dummy video driver for headless environment (no visuals)
os.environ["SDL_AUDIODRIVER"] = "dummy" #Dummy audio driver for headless environment
logging.basicConfig(level=logging.INFO) #Add logging for test feedback


###############################################
#################### TESTS ####################
###############################################
def test_music_assets():
    logging.info("Testing Music Assets")
    assert os.path.exists("SnakeEyes/Assets/Audio/Music/mainMenuLoop.wav")
    assert os.path.exists("SnakeEyes/Assets/Audio/Music/shopLoop.wav")

def test_SFX_assets():
    logging.info("Testing SFX Assets")
    assert os.path.exists("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
    assert os.path.exists("SnakeEyes/Assets/Audio/SFX/cashRegister.mp3")
    assert os.path.exists("SnakeEyes/Assets/Audio/SFX/coindDropLong.mp3")
    assert os.path.exists("SnakeEyes/Assets/Audio/SFX/coinDrop.mp3")
    assert os.path.exists("SnakeEyes/Assets/Audio/SFX/diceRoll.mp3")

def test_character_movement_assets():
    logging.info("Testing Character Movement Assets")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/Jeff-Back.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/Jeff-ForwardAlt1.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/Jeff-Foward.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/Jeff-RightWalk.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/JeffBackAlt1.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/JeffWalkRight Alt1.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/MjBack.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/MjBackAlt.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/MjForward.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/MjForwardAlt1.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/MJRightWalk.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Movement/MjRightWalkAlt1.png")

def test_character_profile_assets():
    logging.info("Testing Character Profile Assets")
    assert os.path.exists("SnakeEyes/Assets/Characters/Profile/Jeff Profile Alt1.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Profile/Jeff Profile.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Profile/mj-profile.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Profile/mj-profileAlt.png")
    assert os.path.exists("SnakeEyes/Assets/Characters/Profile/jeff teach.png")

def test_environment_background_assets():
    logging.info("Testing Environment Background Assets")
    assert os.path.exists("SnakeEyes/Assets/Environment/Background/Background.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Background/MainMenuBackground.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Background/Store_Info_Panel.png")

def test_environment_object_assets():
    logging.info("Testing Environment Object Assets")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/policeCar.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/carP1.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/carP2.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/carP3.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/carP4.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/ABC_Liquor.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/Perris_Jewels.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/RX-Express.png")
    assert os.path.exists("SnakeEyes/Assets/Environment/Objects/Slow_Panda.png")

def test_icon_assets():
    logging.info("Testing Icon Assets")
    assert os.path.exists("SnakeEyes/Assets/Icons/policeBadge.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/badge.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/WadofCash.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/cash.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/Title animated.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/hotDiceModifier.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/luckyStreakModifier.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/shield modifier.png")
    assert os.path.exists("SnakeEyes/Assets/Icons/boost modifier.png")

def test_icon_assets():
    logging.info("Testing Tutorial Assets")
    assert os.path.exists("SnakeEyes/Assets/Tutorial/tutorial 1.png")
    assert os.path.exists("SnakeEyes/Assets/Tutorial/tutorial 3.png")
    assert os.path.exists("SnakeEyes/Assets/Tutorial/tutorial 4.png")
    assert os.path.exists("SnakeEyes/Assets/Tutorial/tutorial 5.png")
    assert os.path.exists("SnakeEyes/Assets/Tutorial/tutorial 6.png")
    assert os.path.exists("SnakeEyes/Assets/Tutorial/tutorial 7.png")

    
def test_GUI_theme():
    logging.info("Testing GUI Theme")
    assert os.path.exists("SnakeEyes/Assets/theme.json")