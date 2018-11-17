from Point2D import *
from math import sin, cos
from bazier import vec2d
class Missile:
    def __init__(self,x ,y):
        self.position = vec2d(x, y)

    def move(self, x, y):
        self.position.y +=  y
        self.position.x += x

    def update(self, rad):
        dx = cos(rad)
        dy = sin(rad)
        self.move(dx, dy)

