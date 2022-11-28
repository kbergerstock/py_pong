# ball.py
# k.r.bergerstock junr 2020
# object class for pong.py

import math
import const
import random
import arcade
from const import sign
from const import EDGES
from arcade import color


class BallSprite(arcade.SpriteCircle):
    __SPEED = 150.0
    __RADIUS = 8

    # create a circle sprite
    def __init__(self):
        super().__init__(BallSprite.__RADIUS, color.ALLOY_ORANGE, False)
        self.set_angle()
        self.speed = BallSprite.__SPEED
        self._dx = 0.0
        self._dy = 0.0
        self.last_edge = 0
        self.last_id = 0
        self.point = False
        self.home()

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
        degrees = random.triangular(25, 85)
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
    # and handles collisions
    # returns true if it collides with out of bounds marker
    # returns fkase otherwise
    def update(self, dt, edges, paddles):
        touched = arcade.check_for_collision_with_list(self, edges)
        if touched:
            edge = touched[0].edge
            if self.last_edge == edge:
                pass
            elif edge == EDGES["top"] or edge == EDGES["bottom"]:
                self.dy *= -1
                self.last_edge = edge
            else:
                for player in paddles:
                    player.point = False
                    if (player.id == 1 and edge == EDGES["player2"]) or (
                        player.id == 2 and edge == EDGES["player1"]
                    ):
                        player.point = True
                        print(player.id, player.point)
                        self.home()
                return True

        for player in paddles:
            tt = arcade.check_for_collision(self, player)
            if tt and self.last_id != player.id:
                self.dx *= -1
                self.set_angle()
                self.speed *= 1.03
                self.last_id = player.id
        self.move(dt)
        return False

    def home(self):
        self.center_y = const.SCREEN_HEIGHT // 2
        self.center_x = const.SCREEN_WIDTH // 2
        self.dx = 0
        self.dy = 0
        self.last_edge = 0

    # def Scored(self, player):
    #     return (self.RIGHT <= 0 and player.id == 2) or (
    #         self.LEFT >= const.SCREEN_WIDTH and player.id == 1
    #     )
