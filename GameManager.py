import pygame
from Player import *
from Missile import *
from enemy import *
from Particle import *
from teleporter import Teleporter

particle = [] # <= (UNIT, set of Particles())
missiles = []
units = []
enemy_types = {"BOSS": 1, "NORMAL": 2}
def collision(missile, units, pvp=False, players=[]):
    for unit in units:
        rect_missile =  pygame.Rect(missile.position.x, missile.position.y, 3, 3)
        rect_unit    =  pygame.Rect(unit.position.x,  unit.position.y, unit.hitbox_size, unit.hitbox_size)
        
        if rect_missile.colliderect(rect_unit) and not unit == missile.player:
            for i in range(0, random.randint(3, 10)):
                particle.append((unit,Particle(missile.position.x, missile.position.y, missile.rad)))
            return (True, unit)

    return(False, None)

def player_unit_collision(unit, players):
    for player in players:
        rect_unit =  pygame.Rect(unit.position.x, unit.position.y, unit.hitbox_size, unit.hitbox_size)
        player_unit    =  pygame.Rect(player.position.x,  player.position.y, player.hitbox_size, player.hitbox_size)
        
        if rect_unit.colliderect(player_unit) and unit != player:
            return True, player

    return False, None

def create_wave(window_size, amount = 1, unit_type = 1):
    x = random.randint(0, window_size[0]) 
    y = random.randint(0, window_size[1])

    if unit_type == 1:
        units.extend([Enemy(random.randint(0, window_size[0]) , random.randint(0, window_size[1]), 1) for unit in range(0, amount)])
    elif unit_type == 2:
        units.extend([Enemy(random.randint(0, window_size[0]) ,random.randint(0, window_size[1]), 2) for unit in range(0, amount)])
    elif unit_type == 3:
        units.extend([Teleporter(random.randint(0, window_size[0]),random.randint(0, window_size[1]), 1) for unit in range(0, amount)])
