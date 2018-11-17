from Point2D import *
from math import sin, cos
from bazier import vec2d
class Missile:
    def __init__(self,x ,y, rad):
        self.position = vec2d(x, y)
        self.rad = rad

    def move(self, x, y):
        self.position.y +=  y
        self.position.x += x

        
    def update(self):
        dx = cos(self.rad) * 6
        dy = -sin(self.rad) * 6
        self.move(dx, dy)

