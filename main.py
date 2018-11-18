
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
import os

HOST = '130.236.181.74'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(0.002)
players = {}
player_id_cnt = 0
os.environ['SDL_VIDEO_CENTERED'] = '1'
def parse_joystick_msg(msg):
    global player_id_cnt
    if "ping" in msg:
        return
    
    if msg[0] == ";":
        msg = msg.split("|")
        st = ""
        if player_id_cnt < 10:
            st = "0" + str(player_id_cnt)
        s.send(st.encode())
        players[st] = Player(300, screen.get_height() - 200, msg[1:])
        player_id_cnt += 1
        return

    id = msg[:2]
    if "CLOSED" in msg or len(players) == 0:
        if id in players:
            del players[id]
        return
    player = players[id]
    msg = msg[2:].split("|")[0]

    if "LEFTSTART" in msg:
        player.power = 22
    elif "LEFTEND" in msg:
        player.power = 0
    elif "RIGHTSTART" in msg:
        pass
    elif "RIGHTEND" in msg:
        pass
    
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
    
    file_path = "./assets/audio/xeno.wav"    
    #play_sound(file_path)

    analyzer = Analyzer(file_path)
    size = width, height = 1080, 920

    info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
    width, height = info.current_w,info.current_h
    window_width,window_height = width-10,height-50
    screen = pygame.display.set_mode((window_width,window_height))
    pygame.display.update()
    black = 0, 0, 0    

    clock = pygame.time.get_ticks() + 50
    clock_temp = pygame.time.get_ticks() + 1000

    units.extend([Enemy(10 + unit * 30,20, 1) for unit in range(0, 12)])
    units.extend([Enemy(10 + unit * 30, 20, 2) for unit in range(0, 30)])
    units.extend([Teleporter(10 + unit * 30, 20, 3) for unit in range(0, 5)])

    clock_2 = pygame.time.Clock()
    tick = 0

    player_img = pygame.image.load("assets/img/charsmall.png")
    player_rect = player_img.get_rect()

    start_time = pygame.time.get_ticks()

    GAME_FONT = pygame.freetype.Font("assets/fonts/Roboto-Italic.ttf", 62)
    text_surface, rect = GAME_FONT.render("goo.gl/HTn5hU", (255, 255, 255))
    inited = False
    
    while True:
        if not inited and len(players) >= 1:
            for unit in units:
                unit.player = players[list(players.keys())[0]]
            inited = True
        
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
            screen.blit(r_image, (player.position.x - 10, player.position.y- 10, 10, 10))

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
            elif missile.position.x > width or missile.position.x < 0 or missile.position.y < 0 or missile.position.y > height:
                missiles.remove(missile)

        screen.blit(text_surface, (width/2 - 100, 10))
        pygame.display.flip()
        pygame.display.update()

