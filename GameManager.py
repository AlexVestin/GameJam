import pygame
from Player import *
from Missile import *
from enemy import *

particle = [] # <= (UNIT, set of Particles())
missiles = []
units = []
enemy_types = {"BOSS": 1, "NORMAL": 2}
def collision(missile, units):
    for unit in units:
        rect_missile =  pygame.Rect(missile.position.x, missile.position.y, 3, 3)
        rect_unit    =  pygame.Rect(unit.position.x,  unit.position.y, unit.size, unit.size)
        if rect_missile.colliderect(rect_unit):
            return (True, unit)

    return(False, None)

def create_wave(player, amount = 1, ):
    units.extend([Enemy(10 + unit * 30,20, 1, player) for unit in range(0, amount)])
