
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
import pygame.freetype

HOST = '130.236.181.74'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(0.002)
players = {}
player_id_cnt = 0

def parse_joystick_msg(msg):
    global player_id_cnt

    print(msg)
    if "ping" in msg:
        return
    
    if msg[0] == ";":
        msg = msg.split("|")
        st = ""
        if player_id_cnt < 10:
            st = "0" + str(player_id_cnt)
        s.send(st.encode())
        players[st] = Player(10, screen.get_height() - 20, msg[1:])
        player_id_cnt += 1
        return

    
    id = msg[:2]
    player = players[id]
    msg = msg[2:].split("|")[0]

    if "LEFTSTART" in msg:
        player.power = 11
    elif "LEFTEND" in msg:
        player.power = 0
    elif "RIGHTSTART" in msg:
        pass
    elif "RIGHTEND" in msg:
        player.rotation = 0
    elif "CLOSED" in msg:
        del players[id]
        return
    
    #right joystick
    if  msg[0] == "_":
        split_msg = msg.split(":")[0][1:]
        player.rotation = float(split_msg)
        #player.power = float(split_msg[2])
    
    #left joystick
    if  msg[0] == "*":
        split_msg = msg.split(":")[0][1:]
        player.direction = float(split_msg)
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
    #play_sound(file_path)

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

    GAME_FONT = pygame.freetype.Font("assets/fonts/Roboto-Italic.ttf", 24)
    text_surface, rect = GAME_FONT.render("goo.gl/HTn5hU", (255, 255, 255))
    
    while True:
        t = pygame.time.get_ticks() -  start_time
        on_beat, strength = analyzer.get_beat(t)

        msg = ""
        for _ in range(len(players) + 1):
            try:
                msg = s.recv(16)
            except:
                pass
        
        if msg:
            parse_joystick_msg(msg.decode())

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        current = pygame.time.get_ticks()
        
        """
        current = pygame.time.get_ticks()
        if current >= clock_temp:
            clock_temp = current + 1000
            create_wave()
        """

        screen.fill(black)

        for key in players.keys():
            player = players[key]
            player.joystick_pressed()
            player.key_pressed()
            player.shoot()
            #if on_beat:
            #    create_wave(player)
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


        screen.blit(text_surface, (1080/2 - 100, 10))
        pygame.display.flip()
        pygame.display.update()

