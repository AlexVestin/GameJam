from Point2D import *
from bazier import *
import random

class Teleporter:
    def __init__(self, x, y, type, player, timestamps):
        self.position = vec2d(x, y)
        self.type = type
        self.hit_points = 10
        self.health()
        self.path = []
        self.size = 0
        self.dead = False
        self.color = None
        self.speed = 0
        self.timestamps = timestamps
        self.player = player
        self.init()

    def init(self):
        self.color = pygame.Color(128,255,80)
        self.size = 10
        self.speed = 2000
    
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

    def update(self, t):
        """
        sec = t / 1000.0
        print(sec, self.timestamps[0][0])
        print(len(self.timestamps))
        if sec > self.timestamps[0][0]:
            ts, strength = self.timestamps.pop()
            self.teleport()

        if self.hit_points <= 0:
            self.dead = True
        """
        pass




