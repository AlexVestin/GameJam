from Point2D import *
from bazier import *
import random, time

class Teleporter:
    def __init__(self, x, y, type, player = None):
        self.position = vec2d(x, y)
        self.type = type
        self.id = None
        self.hit_points = 10
        self.health()
        self.path = []
        self.size = 0
        self.dead = False
        self.color = None
        self.speed = 0
        self.hitbox_size = 20
        self.player = player
        self.amt = 0.4
        self.noise = 100
        self.is_player = False
        self.jump_cd_amt = 8
        self.time_since_beat = 0
        self.init()
        
    def init(self):
        self.color = pygame.Color(128,255,80)
        self.size = 10
        self.speed = 2000
        self.jump_cd = random.randint(1, self.jump_cd_amt)
    
    def teleport(self, player_pos):
        px, py = player_pos.x, player_pos.y
        x, y  = self.position.x, self.position.y
        dx, dy = int((px - x) * random.random() * self.amt), int((py - y) * random.random() * self.amt)
        dx += random.randint(-self.noise, self.noise)
        dy += random.randint(-self.noise, self.noise)

        self.move(dx, dy)

    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    def health(self): # one his =-100
        if self.type == 1: self.hit_points = 200
        elif self.type == 2: self.hit_points = 100

    def update(self, on_beat, t = 0):
         
        if on_beat:
            self.jump_cd -= 1

            if self.player and self.jump_cd == 0:
                #if self.jump_cd == 0:
                self.teleport(self.player.position)
                self.jump_cd = random.randint(1, self.jump_cd_amt)

        if self.hit_points <= 0:
            self.dead = True
        
        




