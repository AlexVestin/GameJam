from Point2D import *
from bazier import *
import random

class Teleporter:
    def __init__(self, x, y, type):
        self.position = vec2d(x, y)
        self.type = type
        self.hit_points = 10
        self.health()
        self.path = []
        self.size = 0
        self.dead = False
        self.color = None
        self.speed = 0
        self.hitbox_size = 20
        self.init()

    def init(self):
        self.color = pygame.Color(128,255,80)
        self.size = 10
        self.speed = 2000
        self.jump_cd = random.randint(1, 8)
    
    def teleport(self):
        x = random.randint(0, 1000)
        y = random.randint(0, 400)
        self.move(x, y)

    def move(self, x, y):
        self.position.x = x
        self.position.y = y

    def health(self): # one his =-100
        if self.type == 1: self.hit_points = 200
        elif self.type == 2: self.hit_points = 100

    def update(self, on_beat):
        if on_beat:
        
            self.jump_cd -= 1
            #if self.jump_cd == 0:
            self.teleport()
            self.jump_cd = random.randint(1, 8)

        if self.hit_points <= 0:
            self.dead = True
        
        




