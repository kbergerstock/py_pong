# ball.py
# k.r.bergerstock junr 2020
# object class for pong.py

import math
import const
import random
import arcade
from const import sign
from const import EDGE
from arcade import color
from icecream import ic


class BallSprite(arcade.SpriteCircle):
    __RADIUS = 10

    # create a circle sprite
    def __init__(self, name):
        super().__init__(BallSprite.__RADIUS, color.ALLOY_ORANGE, False)
        self.set_angle()
        self.speed = const.BALL_VELOCITY
        self._dx = 0.0
        self._dy = 0.0
        self.point = False
        self.home()
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def get_speed(self) -> float:
        return self._speed

    def set_speed(self, velocity: float):
        self._speed = velocity

    speed = property(get_speed, set_speed)

    def get_dy(self):
        return self._dy

    def set_dy(self, v):
        self._dy = sign(v)

    dy = property(get_dy, set_dy)

    def get_dx(self):
        return self._dx

    def set_dx(self, v):
        self._dx = sign(v)

    dx = property(get_dx, set_dx)

    def set_angle(self):
        degrees = random.triangular(30, 85)
        self._angle = float(degrees) * math.pi / 180.0
        self._cos = math.cos(self._angle)
        self._sin = math.sin(self._angle)

    @property
    def COSINE(self):
        return self._cos

    @property
    def SINE(self):
        return self._sin

    def move(self, dt):
        self.center_x += self.SINE * self.speed * dt * self.dx
        self.center_y += self.COSINE * self.speed * dt * self.dy

    # updates the ball location
    # and handles collisions`
    # returns true if it collides with out of bounds marker
    # returns false otherwise
    def update(self, dt, sprites: arcade.SpriteList, server: int):
        player = None
        touched = arcade.check_for_collision_with_list(self, sprites)
        if touched:
            ic(touched[0].name)
            if touched[0].name == "top" or touched[0].name == "bottom":
                self.dy *= -1
            elif touched[0].name == "ply1":
                sprites[EDGE["ply1"]].point = False
                self.set_angle()
                self.dx *= -1
                self.dy *= -1
            elif touched[0].name == "ply2":
                sprites[EDGE["ply2"]].point = False
                self.set_angle()
                self.dx *= -1
                self.dy *= -1
            elif touched[0].name == "end1":
                self.home()
                sprites[EDGE["ply2"]].point = False
                if sprites[EDGE["ply2"]].id == server:
                    sprites[EDGE["ply2"]].point = True
                return True, "ply2"
            elif touched[0].name == "end2":
                self.home()
                sprites[EDGE["ply1"]].point = False
                if sprites[EDGE["ply1"]].id == server:
                    sprites[EDGE["ply1"]].point = True
                return True, "ply1"
        self.move(dt)
        return False, False

    def home(self):
        self.center_y = const.SCREEN_HEIGHT // 2
        self.center_x = const.SCREEN_WIDTH // 2
        self.dx = 0
        self.dy = 0
