import pygame
from SnakeEyes.Code import CPU
class Player:
    def __init__(self):
        self.tmpScore = 0
        self.score = 0
        self.status = 0 #-1 - cashed out | 0 - waiting | 1 ready
        self.playerNum = 0
        self.controller = None
        self.color = (255, 0, 0)
        self.position = pygame.Vector2(640, 360)
        self.collider = pygame.Rect(0,0,100,100)
        self.collider.center = self.position
        self.XCol = pygame.Rect(0,0,10,10)
        self.XCol.center = self.position
        self.YCol = pygame.Rect(0,0,10,10)
        self.YCol.center = self.position
        self.modSelection = 0
        self.currentMods = {}
        self.streak = 0
        self.scoreText = ""
        

        ##### STATUS #####
        self.gr = pygame.Vector2(0, 0)
        self.yl = pygame.Vector2(0, 0)
        self.rd = pygame.Vector2(0, 0)

        ##### Controlls #####
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.ready = pygame.K_1
        ##self.cashOut = pygame.K_2
        #store status locations for programatic access

        self.CPU = CPU.CPU()