#Makes file imports able to be done from the root
#This makes file paths compatible with the paths our tests expect
import sys
import os

#Get the absolute path of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#Set GammaRepo's path
gamma_repo_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
#Change the working directory to GammaRepo
os.chdir(gamma_repo_path)
print(f"Working directory set to: {os.getcwd()}") #Debug
sys.path.append(gamma_repo_path)

import pygame
from SnakeEyes.Code.scene_manager import SceneManager

def main():
    pygame.init()
    sceneManager = SceneManager()
    sceneManager.run()

if __name__ == "__main__":
    main()