from Point2D import *
class Missile:
    def __init__(self,x ,y):
        self.position = Point2D(x, y)

    def move(self, x, y):
        self.position.y +=  y

    def update(self):
        self.move(0,-1)

