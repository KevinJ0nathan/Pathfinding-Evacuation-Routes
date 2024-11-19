import pygame
from constants import *

class Survivor:
    def __init__(self, start_spot, color=BLUE, width=10):
        self.current_spot = start_spot
        self.color = color
        self.width = width
        self.x = start_spot.x
        self.y = start_spot.y
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.current_spot.width, self.current_spot.width))

    def move_to(self, new_spot):
        self.current_spot = new_spot
        self.x = new_spot.x
        self.y = new_spot.y