import pygame
from Player import *
from Missile import *

missiles = []

def collision(missile, units):
    for unit in units:
        rect_missile =  pygame.Rect(missile.position.x, missile.position.y, 3, 3)
        rect_unit    =  pygame.Rect(unit.position.x,  unit.position.y, 3, 3)
        if rect_missile.collidedict(rect_unit):
            return (True, unit)
            pass
