import pygame
from Player import *
from Missile import *
from enemy import *
from Particle import *

particle = [] # <= (UNIT, set of Particles())
missiles = []
units = []
enemy_types = {"BOSS": 1, "NORMAL": 2}
def collision(missile, units):
    for unit in units:
        rect_missile =  pygame.Rect(missile.position.x, missile.position.y, 3, 3)
        rect_unit    =  pygame.Rect(unit.position.x,  unit.position.y, unit.hitbox_size, unit.hitbox_size)
        if rect_missile.colliderect(rect_unit):
            for i in range(0, random.randint(3, 10)):
                particle.append((unit,Particle(missile.position.x, missile.position.y, missile.rad)))
            return (True, unit)

    return(False, None)

def create_wave(player, amount = 1, ):
    units.extend([Enemy(10 + unit * 30,20, 1, player) for unit in range(0, amount)])
