import pygame
class Car:
    def __init__(self):
        self.playerNum = 0
        self.position = pygame.Vector2(0, 0)
        self.collider = pygame.Rect(self.position.x, self.position.y, 0,150)
        self.rb = pygame.Rect(self.position.x, self.position.y, 60,150)
        self.carSprite = pygame.image.load('SnakeEyes/Assets/Environment/Objects/carP1.png')
        self.ready = False