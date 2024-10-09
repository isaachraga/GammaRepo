#Makes file imports able to be done from the root
#This makes file paths compatible with the paths our tests expect
import sys, os
sys.path.append(os.path.abspath('')) 

import pygame
from SnakeEyes.Code.scene_manager import SceneManager

def main():
    pygame.init()
    sceneManager = SceneManager()
    sceneManager.run()

if __name__ == "__main__":
    main()