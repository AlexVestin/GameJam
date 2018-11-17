from Point2D import *
from bazier import *
import random
class Enemy:
    def __init__(self,x, y, type):
        self.position = Point2D(x, y)
        self.type = type
        self.health()
        self.hit_points = 0
        self.path = []
        self.set_path()

    def set_path(self):
        #Move bezier here
        random_x = random.randint(0, 500)
        random_y = random.randint(0, 500)
        #Might have to remember the previous random X and offset from the prev
        control_points = [vec2d(self.position.x + random.randint(0, 500), self.position.y + random.randint(0, 500)),
                          vec2d(self.position.x + random.randint(0, 500), self.position.y + random.randint(0, 500)),
                          vec2d(self.position.x + random.randint(0, 500), self.position.y + random.randint(0, 500)),
                          vec2d(self.position.x + random.randint(0, 500), self.position.y + random.randint(0, 500))]
        self.path = compute_bezier_points([(x.x, x.y) for x in control_points])
        self.path.reverse()# USE THIS AS PATH

    def move(self, x, y):
        if len(self.path) != 0:
            move_to = self.path.pop()
            self.position.x = move_to[0]
            self.position.y = move_to[1]
        else:
            self.set_path()


    def health(self):
        if self.type == 1: self.hit_points = 145
        elif self.type == 2: self.hit_points = 100


