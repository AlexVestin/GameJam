from Point2D import *

class Enemy:
    def __init__(self,x, y, type):
        self.position = Point2D(x, y)
        self.type = type
        self.health()
        self.hit_points = 0

    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    def health(self):
        if self.type == 1: self.hit_points = 145
        elif self.type == 2: self.hit_points = 100


