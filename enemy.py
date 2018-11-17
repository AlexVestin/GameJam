from Point2D import *

class Enemy:
    def __init__(self,x, y):
        self.position = Point2D(x, y)

    def move(self, x, y):
        self.position.x += x
        self.position.y += y

