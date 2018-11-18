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
        
        if rect_missile.colliderect(rect_unit) and not unit.is_player:
            for i in range(0, random.randint(3, 10)):
                particle.append((unit,Particle(missile.position.x, missile.position.y, missile.rad)))
            return (True, unit)

    return(False, None)

def player_unit_collision(unit, players):
    for player in players:
        rect_unit =  pygame.Rect(unit.position.x, unit.position.y, unit.hitbox_size, unit.hitbox_size)
        player_unit =  pygame.Rect(player.position.x,  player.position.y, player.hitbox_size, player.hitbox_size)
        
        if rect_unit.colliderect(player_unit) and unit != player:
            return True, player

    return False, None



SAFE_DISTANCE = 30
def get_spawn_coords(window_size, players):
    
    safe_distance = False
    x = y = 0
    while not safe_distance:
        x = random.randint(0, window_size[0]) 
        y = random.randint(0, window_size[1])

        for player in players: 
            if abs(player.position.y - y) < SAFE_DISTANCE: continue
            if abs(player.position.y - y) < SAFE_DISTANCE: continue
        
        safe_distance = True
    
    return x, y


def spawn_enemies(amt, t, Class, players, window_size):
    for i in range(0, amt):
        x, y = get_spawn_coords(window_size, players)
        units.append(Class(x, y, t))

def create_wave(window_size, amount, unit_type, players):
    if unit_type == 1 or unit_type == 2:
        spawn_enemies(amount, unit_type, Enemy, players, window_size)
    elif unit_type == 3:
        spawn_enemies(amount, unit_type, Teleporter, players, window_size)
  