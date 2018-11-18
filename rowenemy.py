from Point2D import *
from bazier import *
import random, time

class RowEnemy:
    def __init__(self, x, y, type, player = None):
        self.position = vec2d(x, y)
        self.type = type
        self.id = None
        self.hit_points = 10
        self.health()
        self.path = []
        self.size = 0
        self.type = type
        self.dead = False
        self.color = None
        self.speed = 0
        self.hitbox_size = 20
        self.player = player
        self.score_on_death = 90
        self.amt = 0.4
        self.noise = 100
        self.is_player = False
        self.jump_cd_amt = 8
        self.time_since_beat = 0
        self.impact_damage = 50
        self.init()
        
    def init(self):
        self.color = pygame.Color(128,255,80)
        self.size = 10
        self.speed = 2000
    
    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    def health(self): # one his =-100
        if self.type == 1: self.hit_points = 200
        elif self.type == 2: self.hit_points = 100

    def update(self, on_beat, t = 0):
        self.move(0, 1)
        




