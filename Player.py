import pygame
from Point2D import *
from GameManager import *
from Missile import *
from bazier import vec2d
import math

class Player():
    def __init__(self, x, y, name, id):
        self.name = name
        self.id = id
        self.position = vec2d(x, y)
        self.points = 0
        self.cooldown = 75
        self.color = None
        self.last_fired = pygame.time.get_ticks()
        self.left_joystick_down = False
        self.right_joystick_down = False
        self.direction = 0
        self.power = 0
        self.rotation = 0
        self.hit_points = 200
        self.score = 0
        self.max_hit_points = 200
        self.hitbox_size = 20
        self.dead = False
        self.score_on_death = 500
        self.is_player = True

    def update(self, on_beat):
        pass

    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    def shoot(self):
        if self.check_cooldown():
            missiles.append(Missile(self.position.x + 10, self.position.y + 10, self.rotation, self))

    def joystick_pressed(self):
        dx = math.cos(self.direction) * self.power / 12
        dy = -math.sin(self.direction) * self.power / 12
        self.move(dx, dy)

    def key_pressed(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.move(-1 , 0)
            if self.position.x == -1:
                self.position.x = 0
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
            if self.position.x == 420:
                self.position.x = 420
        if keys[pygame.K_SPACE]:
            if self.check_cooldown():
               self.shoot()

    def check_cooldown(self):
        if  pygame.time.get_ticks() - self.last_fired >= self.cooldown:
            self.last_fired = pygame.time.get_ticks()
            return True

        return False


