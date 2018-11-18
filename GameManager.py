import pygame
from Player import *
from Missile import *
from enemy import *

particle = [] # <= (UNIT, set of Particles())
missiles = []
units = []
enemy_types = {"BOSS": 1, "NORMAL": 2}
def collision(missile, units, pvp=False, players=[]):
    for unit in units:
        rect_missile =  pygame.Rect(missile.position.x, missile.position.y, 3, 3)
        rect_unit    =  pygame.Rect(unit.position.x,  unit.position.y, unit.hitbox_size, unit.hitbox_size)
        
        if rect_missile.colliderect(rect_unit) and not unit == missile.player:
            return (True, unit)

    return(False, None)

def player_unit_collision(unit, players):
    for player in players:
        rect_unit =  pygame.Rect(unit.position.x, unit.position.y, unit.hitbox_size, unit.hitbox_size)
        player_unit    =  pygame.Rect(player.position.x,  player.position.y, player.hitbox_size, player.hitbox_size)
        
        if rect_unit.colliderect(player_unit):
            return True, player

    return False, None

def create_wave(player, amount = 1, ):
    units.extend([Enemy(10 + unit * 30,20, 1, player) for unit in range(0, amount)])
