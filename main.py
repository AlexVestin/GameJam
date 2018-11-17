
import sys, pygame
from Player import *
from enemy import *
from GameManager import *
from bazier import *
import socket, math
from analyze_audio import *
import pickle

HOST = '130.236.181.73'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(0.00005)

def parse_joystick_msg(msg, player):
    if "ping" in msg:
        return
    
    splt = msg.split("|")
    if splt[1]:
        last_msg = splt[1]
    else:
        last_msg = splt[0]
    if "LEFTSTART" in msg:
        player.power = 11        
    elif "LEFTEND" in msg:
        player.power = 0
    elif "RIGHTSTART" in msg:
        pass
    elif "RIGHTEND" in msg:
        player.rotation = 0
    
    #right joystick
    if  last_msg[0] == "_":
        split_msg = msg.split(":")
        player.rotation = float(split_msg[1])
        #player.power = float(split_msg[2])
    
    #left joystick
    if  last_msg[0] == "*":
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
    
    """
    audio_info, tempo = analyze_audio(file_path)
    with open("audio.txt", "wb") as f:
        f.write(pickle.dumps(audio_info))
    """

    tempo = 112.3471
    f = open("audio.txt", "rb")
    audio_info = pickle.load(f)
    f.close()
    play_sound(file_path)

    size = width, height = 1080, 420
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    screen.get_height()
    player = Player(10, screen.get_height() - 20)

    clock = pygame.time.get_ticks() + 50
    clock_temp = pygame.time.get_ticks() + 1000

    units.extend([Enemy(10 + unit * 30,20, 1) for unit in range(0, 30)])

    clock_2 = pygame.time.Clock()
    prev_speed = 1
    tick = 0

    player_img = pygame.image.load("assets/img/charsmall.png")
    player_rect = player_img.get_rect()

    while True:
        msg = ""
        try:
            msg = s.recv(12)
        except:
            pass
        
        if msg:
            parse_joystick_msg(msg.decode(), player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        current = pygame.time.get_ticks()

        for unit in units:
            unit.move(0, 1)
        if current >= clock:
            clock = current + 20


        """
        current = pygame.time.get_ticks()
        if current >= clock_temp:
            clock_temp = current + 1000
            create_wave()
            """

        player.joystick_pressed()
        player.key_pressed()
        

        r_image = rot_center(player_img, ((player.rotation - (math.pi/2)) / math.pi) * 180 )

        screen.fill(black)
        screen.blit(r_image, (player.position.x - 20, player.position.y- 20, 20, 20))
        pygame.draw.rect(screen, pygame.Color(0,0,128), pygame.Rect(player.position.x, player.position.y, 12, 12), 5)

        for unit in units:
            # Draw each path
            pygame.draw.rect(screen, pygame.Color(0, 128, 0), pygame.Rect(unit.position.x, unit.position.y, 5, 5), 5)

        for missile in missiles:
            missile.update()
            occured_collision = collision(missile, units)
            pygame.draw.rect(screen, pygame.Color(128, 0, 0), pygame.Rect(missile.position.x, missile.position.y, 3, 3), 3)
            if occured_collision[0]:
                print(occured_collision)
                missiles.remove(missile)
                units.remove(occured_collision[1])

        pygame.display.flip()
        pygame.display.update()

