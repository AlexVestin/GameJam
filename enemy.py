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
        self.score_on_death = 0
        self.hitbox_size = 0
        self.is_player = False
        self.player = player
        self.impact_damage = 0
        self.pulse = False
        self.prev_pulse = 1
        self.init()

    def init(self):
        if self.type == 1: #Boss
            self.color = pygame.Color(128,128,0)
            self.size = 10
            self.speed = 500
            self.hitbox_size = 10
            self.set_path()
            self.score_on_death = 120
            self.impact_damage = 80
        else:
            self.size = 3
            self.score_on_death = 30
            self.hitbox_size = 8
            self.speed = 200
            self.color = pygame.Color(0,128,128)
            self.impact_damage = 20
            self.set_path()

    def reset_size(self):
        if self.type == 1:
            self.size = 10
        else:
            self.size = 3

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
        if self.type == 1: self.hit_points = 120
        elif self.type == 2: self.hit_points = 70

    def on_pulse(self):
        if self.size <= 6 and self.prev_pulse != -1:
            self.size += 1
            self.prev_pulse = 1
        else:
            if self.size > 0:
                self.size -= 1
                self.prev_pulse = -1



    def update(self, onbeat, strength):
        if onbeat:
            self.pulse = True
            self.reset_size()
            self.prev_pulse = 1

        if self.pulse:
            self.on_pulse()

        self.move(0, 1)
        if self.hit_points <= 0:
            self.dead = True




