import pygame
class Store:
    def __init__(self):
        self.num1 = 0
        self.num2 = 0
        self.storeNum = 0
        self.scoreText = ""
        self.scoreTextColor = (255,255,255)
        self.status = 0 #0 - ready | -1 alarmed
        self.color = (0,0,255)
        self.position = pygame.Vector2(0, 0)
        #risk/reward are scales that go from 1-5 that modify roll information
        self.risk = 0
        self.reward = 0
        self.collider = pygame.Rect(self.position.x, self.position.y, 0, 0) # Changed in StoreReset()
        self.players = []
        self.sprite = ""