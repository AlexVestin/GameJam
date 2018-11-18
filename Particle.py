from bazier import vec2d
from math import cos, sin
import random

class Particle():
    def __init__(self, x, y, rad):
        #Spawn particles at collision hit
        self.position = vec2d(x, y)
        self.rad = rad + random.random() * random.randint(-1, 1)
        self.alpha = 255
        self.speed = 0
        self.type = random.randint(0, 2)
        #0 = linger, 1 = active
        #Typer av partiklar, those that linger and those that do not

    def speed(self):
        if self.type == 0: self.speed = 1
        else: self.speed = 10

    def move(self,x ,y):
        self.position.x += x
        self.position.y += y

    def update(self):
        dx =   cos(self.rad) * self.speed
        dy = - sin(self.rad) * self.speed
        if self.alpha-10 >= 0:
            self.alpha -= 10
        self.move(dx, dy)
