import pygame
#from core import Game
#from coreV2 import Game
from scene_manager import SceneManager


def main():
    pygame.init()
    sceneManager = SceneManager()
    sceneManager.run()

if __name__ == "__main__":
    main()