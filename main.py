
import sys, pygame
from Player import *
from enemy import *
from GameManager import *
from bazier import *
import socket, math
from analyze_audio import *
from teleporter import Teleporter
import pickle
import time

HOST = '130.236.181.74'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(0.00005)
players = {}
player_id_cnt = 0

def parse_joystick_msg(msg):
    global player_id_cnt

    print(msg)
    if "ping" in msg:
        return
    
    if msg[0] == ";":
        msg = msg.split("|")
        players[player_id_cnt] = Player(10, screen.get_height() - 20, msg[1:])
        s.sendall(str(player_id_cnt).encode())
        player_id_cnt += 1
        return


    id = msg.split("?")[0]
    player = players[id]
    msg = msg.split("|")[0]

    if "LEFTSTART" in msg:
        player.power = 11
    elif "LEFTEND" in msg:
        player.power = 0
    elif "RIGHTSTART" in msg:
        pass
    elif "RIGHTEND" in msg:
        player.rotation = 0
    
    #right joystick
    if  msg[0] == "_":
        split_msg = msg.split(":")
        player.rotation = float(split_msg[1])
        #player.power = float(split_msg[2])
    
    #left joystick
    if  msg[0] == "*":
        split_msg = msg.split(":")
        player.direction = float(split_msg[1])
        #player.power = float(split_msg[2])

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

if __name__ == "__main__":
    pygame.init()
    
    file_path = "./assets/audio/Knock.wav"    
    play_sound(file_path)

    analyzer = Analyzer(file_path)

    size = width, height = 1080, 420
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    screen.get_height()


    clock = pygame.time.get_ticks() + 50
    clock_temp = pygame.time.get_ticks() + 1000

    #units.extend([Enemy(10 + unit * 30,20, 1, player) for unit in range(0, 12)])
    #units.extend([Enemy(10 + unit * 30, 20, 2, player) for unit in range(0, 30)])
    #units.extend([Teleporter(10 + unit * 30, 20, 3, player) for unit in range(0, 5)])

    clock_2 = pygame.time.Clock()
    prev_speed = 1
    tick = 0

    player_img = pygame.image.load("assets/img/charsmall.png")
    player_rect = player_img.get_rect()

    start_time = pygame.time.get_ticks()
    while True:
        t = pygame.time.get_ticks() -  start_time
        on_beat, strength = analyzer.get_beat(t)

        msg = ""
        try:
            msg = s.recv(12)
        except:
            pass
        
        if msg:
            parse_joystick_msg(msg.decode())

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        current = pygame.time.get_ticks()
        player.shoot()


        if on_beat:
            create_wave(eplayr)

        screen.fill(black)

        for key in players.keys():
            player = players[key]
            player.joystick_pressed()
            player.key_pressed()
            r_image = rot_center(player_img, ((player.rotation - (math.pi/2)) / math.pi) * 180 )
            screen.blit(r_image, (player.position.x - 20, player.position.y- 20, 20, 20))

        #pygame.draw.rect(screen, pygame.Color(0,0,128), pygame.Rect(player.position.x, player.position.y, 12, 12), 5)

        for unit in units:
            unit.update(on_beat)
            # Draw each path
            if unit.dead:
                units.remove(unit)
            pygame.draw.rect(screen, unit.color, pygame.Rect(unit.position.x, unit.position.y, unit.size, unit.size), unit.size)

        for missile in missiles:
            missile.update()
            occured_collision = collision(missile, units)
            pygame.draw.rect(screen, pygame.Color(128, 0, 0), pygame.Rect(missile.position.x, missile.position.y, 3, 3), 3)
            if occured_collision[0]:
                missiles.remove(missile)
                occured_collision[1].hit_points -= 100

        pygame.display.flip()
        pygame.display.update()

