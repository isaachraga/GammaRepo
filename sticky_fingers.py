#Entry point for packaging project
#To package manually, run:
#    'python -m PyInstaller --onefile --windowed --add-data="Fonts;Fonts" --add-data="SnakeEyes;SnakeEyes" .\sticky_fingers.py'

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) #Get the absolute path of the current file's directory
gamma_repo_path = os.path.abspath(os.path.join(current_dir)) #Set file path
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