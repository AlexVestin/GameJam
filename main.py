
import sys, pygame
from LightSource import *
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
import os, select

HOST = '130.236.181.74'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(0.002)
players = {}
player_id_cnt = 0
os.environ['SDL_VIDEO_CENTERED'] = '1'


colors = ["red", "green", "blue", "white", "pink", "yellow"]

while 1:
    inputready, o, e = select.select([s],[],[], 0.0)
    if len(inputready)==0: break
    for s in inputready: s.recv(1)

def parse_joystick_msg(msg):
    global player_id_cnt
    global units

    if "ping" in msg:
        return
    
    if msg[0] == ";":
        msg = msg.split("|")[0]
        st = ""
        if player_id_cnt < 10:
            st = "0" + str(player_id_cnt)
        s.send(st.encode())
        players[st] = Player(300, screen.get_height() - 200, msg[1:], st)
        player_id_cnt += 1
        units.append(players[st])

        for color in colors:
            if color not in [unit.color for unit in units if unit.is_player]:
                players[st].color = color
                break; 

        return

        if not players[st].color:
            players[st].color = "blue"

    if not len(players):
        return

    id = msg[:2]
    if len(players) == 0:
        return
    if "CLOSED" in msg:
        if id in players:
            del players[id]
        units = [x for x in units if x.id != id]
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
        player.power = 22
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

    LIGHT_GROUP = pygame.sprite.Group()
    All = pygame.sprite.RenderUpdates()
    ShowLight.containers = LIGHT_GROUP, All
    ShowLight.images = pygame.Surface((1, 1), 32)

    for light in LIGHTS:
        if light[0] == 'Spotlight5':
            threading.Timer(random.randint(2, 7), ShowLight, args=(light,)).start()
        else:
            ShowLight(light)

    def segment_adjustment(polygon):
        segments = ALL_SEGMENTS.copy()
        for seg in polygon:
            segments.remove(seg)
        return segments

    shadows = [Shadow(segment_adjustment(POLYGON2), static_=True, location_=(370, 94)),    # LIGHT1
               Shadow(segment_adjustment(POLYGON1), static_=True, location_=(150, 185)),   # LIGHT6                   # LIGHT5
               ]

    global UPDATE
    UPDATE = False

    file_path = "./assets/audio/xeno.wav"
    play_sound(file_path)

    analyzer = Analyzer(file_path)

    clock = pygame.time.get_ticks() + 50
    clock_temp = pygame.time.get_ticks() + 1000

    units.extend([Enemy(10 + unit * 30,20, 1) for unit in range(0, 12)])
    units.extend([Enemy(10 + unit * 30, 20, 2) for unit in range(0, 30)])
    units.extend([Teleporter(10 + unit * 30, 20, 3) for unit in range(0, 5)])

    clock_2 = pygame.time.Clock()
    tick = 0


    player_sprites = {
        "white": pygame.image.load("assets/img/white.png"),
        "blue": pygame.image.load("assets/img/blue.png"),
        "yellow": pygame.image.load("assets/img/yellow.png"),
        "pink": pygame.image.load("assets/img/pink.png"),
        "green": pygame.image.load("assets/img/green.png"),
        "red": pygame.image.load("assets/img/red.png")
    }

    start_time = pygame.time.get_ticks()

    GAME_FONT = pygame.freetype.Font("assets/fonts/Roboto-Italic.ttf", 62)
    GAME_FONT_SMALL = pygame.freetype.Font("assets/fonts/Roboto-Italic.ttf", 30)
    GAME_FONT_SMALLER = pygame.freetype.Font("assets/fonts/Roboto-Italic.ttf", 18)

    text_surface, rect = GAME_FONT.render("goo.gl/HTn5hU", (255, 255, 255))
    inited = False

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

        All.update()

        if CreateLight.UPDATE:

            All.draw(screen)
            CreateLight.UPDATE = False
            for shadow in shadows:
                shadow.render_frame()


        if on_beat:
            create_wave((window_width, window_height), 1, random.randint(1, 3))

        screen.fill(black)

        for p in particle:
            p[1].update()
            pygame.draw.rect(screen, pygame.Color(0,p[1].alpha,0, p[1].alpha), pygame.Rect(p[1].position.x, p[1].position.y, 2, 2),
                             2)

            if p[1].alpha - 10 <= 0: particle.remove(p)

        for key in players.keys():
            player = players[key]
           

            if not player.dead:
                player.joystick_pressed()
                player.key_pressed()
                player.shoot()
                r_image = rot_center(player_sprites[player.color], ((player.rotation - (math.pi/2)) / math.pi) * 180 )
                screen.blit(r_image, (player.position.x, player.position.y, 20, 20))

        for unit in units:
            if not unit.is_player and [unit for unit in units if unit.is_player and not unit.dead]:
                if not unit.player or unit.player.dead:
                    _players = [unit for unit in units if  not unit.dead and unit.is_player ]
                    if players:
                        unit.player = _players[random.randint(0, len(players) - 1)]


            unit.update(on_beat)
            collision_with_player = player_unit_collision(unit, [players[key] for key in list(players.keys())])
            if collision_with_player[0]:
                player = collision_with_player[1]
                player.hit_points -= unit.impact_damage

                if not unit.is_player:
                    unit.dead = True

                if player.hit_points <= 0:
                    player.dead = True
            
            if not unit.is_player:
                pygame.draw.rect(screen, unit.color, pygame.Rect(unit.position.x, unit.position.y, unit.size, unit.size), unit.size)

        for missile in missiles:
            missile.update()
            occured_collision = collision(missile, units)
            pygame.draw.rect(screen, pygame.Color(128, 0, 0), pygame.Rect(missile.position.x, missile.position.y, 3, 3), 3)
            
            if occured_collision[0]:
                missiles.remove(missile)
                occured_collision[1].hit_points -= 100

                    # Draw each path
                if occured_collision[1].hit_points < 0:
                    unit.dead = True
                    if unit in units:
                        units.remove(unit)
                    missile.player.score += unit.score_on_death 

            elif missile.position.x > width or missile.position.x < 0 or missile.position.y < 0 or missile.position.y > height:
                missiles.remove(missile)

        for i, key in enumerate(players.keys()):
            player = players[key]
            if player.hit_points <= 0 or player.dead:
                units = [unit for unit in units if unit.id != player.id] 
            
            #hp_text_surface, rect = GAME_FONT_SMALL.render(player.name + ": " + str(100*player.hit_points/player.max_hit_points).split(".")[0]+"%", (255, 255, 255))
            hp_text_surface, rect = GAME_FONT_SMALL.render(player.name + ": " + str(player.hit_points), (255, 255, 255))
            
            score_text_surface, rect = GAME_FONT_SMALLER.render(str(player.score), (255, 255, 255))
            screen.blit(hp_text_surface, ( (i+1) * 250, 40))
            screen.blit(score_text_surface, ( (i+1) * 250, 78))

        TIME_PASSED_SECONDS = pygame.time.Clock().tick()

        FRAME += 1
        screen.blit(text_surface, (width/2 - 200, 10))

        pygame.display.flip()
        pygame.display.update()

