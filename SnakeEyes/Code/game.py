import pygame
from scene_manager import SceneManager

def main():
    pygame.init()
    sceneManager = SceneManager()
    sceneManager.run()

if __name__ == "__main__":
    main()