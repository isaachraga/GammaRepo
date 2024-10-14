#Makes file imports able to be done from the root
#This makes file paths compatible with the paths our tests expect
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) #Get the absolute path of the current file's directory
gamma_repo_path = os.path.abspath(os.path.join(current_dir, '..', '..')) #Set file path
os.chdir(gamma_repo_path) #Change the working directory to GammaRepo
sys.path.append(gamma_repo_path)

import pygame
from SnakeEyes.Code.scene_manager import SceneManager

def main():
    pygame.init()
    pygame.mixer.init()
    sceneManager = SceneManager()
    sceneManager.run()

if __name__ == "__main__":
    main()