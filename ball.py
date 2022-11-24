# ball.py
# k.r.bergerstock junr 2020
# object class for pong.py

import math
import const
import random
import arcade
from const import sign
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
        self.home()

    def get_speed(self):
        return self._speed

    def set_speed(self, velocity):
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
        degrees = random.randrange(25, 85)
        self._angle = float(degrees) * math.pi / 180.0
        self._cos = math.cos(self._angle)
        self._sin = math.sin(self._angle)

    @property
    def COSINE(self):
        return self._cos

    @property
    def SINE(self):
        return self._sin

    def update(self, dt):
        self.center_x += self.COSINE * self.speed * dt * self.dx
        self.center_y += self.SINE * self.speed * dt * self.dy

    #  handle a wall collision
    #  detect upper and lower screen boundary collision, playing a sound
    #  effect and reversing dy if true
    # def handleWallCollision(self):
    #     if self.BOTTOM <= 0 or self.TOP >= const.SCREEN_HEIGHT:
    #         self.dy *= -1
    #         self.set_position(self.center_x, self.center_y + 1 * self.dy)
    #         return True
    #     else:
    #         return False

    # def handlePaddleCollision(self, player):
    #     if arcade.check_for_collision(self, player):
    #         self.dx = self.dx * -1
    #         self.set_angle()
    #         self.center_x = self.center_x + 1 * self.dx
    #         return True
    #     else:
    #         return False

    def home(self):
        self.center_y = const.SCREEN_HEIGHT // 2
        self.center_x = const.SCREEN_WIDTH // 2
        self.dx = 0
        self.dy = 0

    def render(self):
        self.draw()

    # # handle the ball serve
    # def Serve(self, player):
    #     # before switching to play, initialize ball's velocity based
    #     # on player who last scored
    #     self.dy = random.choice([-1, 1])
    #     self.dx = 1 if player.id == 1 else -1
    #     self.speed = BALL.__SPEED
    #     self.set_angle()
    #     self.home(player)

    # def Scored(self, player):
    #     return (self.RIGHT <= 0 and player.id == 2) or (
    #         self.LEFT >= const.SCREEN_WIDTH and player.id == 1
    #     )
