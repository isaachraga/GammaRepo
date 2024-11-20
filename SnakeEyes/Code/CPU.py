import pygame

class CPU:
    def __init__(self):
        self.moveToLocation = (0,0)
        self.turn = 0
        self.previousScore = 0
        self.counter = 0
    #   self.low_threshold = 0
    #   self.high_threshold = 0