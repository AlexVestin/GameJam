from Point2D import *
from bazier import *
import random
class Enemy:
    def __init__(self, x, y, type, player = None):
        self.position = vec2d(x, y)
        self.id = None
        self.type = type
        self.hit_points = 0
        self.health()
        self.path = []
        self.size = 0
        self.dead = False
        self.color = None
        self.speed = 0
        self.hitbox_size = 0
        self.is_player = False
        self.player = player
        self.init()

    def init(self):
        if self.type == 1: #Boss
            self.color = pygame.Color(128,128,0)
            self.size = 10
            self.speed = 1000
            self.hitbox_size = 15
            self.set_path()
        else:
            self.size = 3
            self.hitbox_size = 8
            self.speed = 500
            self.color = pygame.Color(0,128,128)
            self.set_path()

    def set_path(self):
        if self.player:
            player_vec = vec2d(self.player.position.x, self.player.position.y) - self.position
            control_points = [vec2d(self.position.x, self.position.y),
                              vec2d(self.position.x + random.randint(-200, 200),
                                    self.position.y + random.randint(-200, 200)) + player_vec,
                              vec2d(self.position.x + random.randint(-200, 200),
                                    self.position.y + random.randint(-200, 200)) + player_vec,
                              vec2d(self.position.x + random.randint(-200, 200),
                                    self.position.y + random.randint(-200, 200)) + player_vec]
            self.path = compute_bezier_points([(x.x, x.y) for x in control_points], self.speed)
            self.path.reverse()  # USE THIS AS PATH


    def move(self, x, y):
        if len(self.path) != 0:
            move_to = self.path.pop()
            self.position.x = move_to[0]
            self.position.y = move_to[1]
        else:
            if self.player:
                self.set_path()
                self.move(0,1)

    def death_animation(self):
        control_points = [vec2d(self.position.x, self.position.y),
                          vec2d(self.position.x + random.randint(-200, 200) , self.position.y + random.randint(-200, 200)) + player_vec,
                          vec2d(self.position.x + random.randint(-200, 200), self.position.y + random.randint(-200, 200)) + player_vec,
                          vec2d(self.position.x + random.randint(-200, 200) , self.position.y + random.randint(-200, 200)) + player_vec]
        self.path = compute_bezier_points([(x.x, x.y) for x in control_points], self.speed)
        self.path.reverse()# USE THIS AS PATH
        pass

    def health(self): # one his =-100
        if self.type == 1: self.hit_points = 200
        elif self.type == 2: self.hit_points = 100

    def update(self, onbeat):
        self.move(0, 1)
        if self.hit_points <= 0:
            self.dead = True




