# ball.py
# k.r.bergerstock junr 2020
# object classes for pong.py
import math
import arcade
from arcade import color
from const import sign
from const import EDGE
from create_texture import create_texture


class Paddle(arcade.BasicSprite):
    __SPEED = 600

    def __init__(self, id: int, k=["ANDROID_GREEN", color.ANDROID_GREEN], name="ply1"):
        super().__init__(create_texture(18, 80, k))
        self._speed = Paddle.__SPEED
        self._score = 0
        self._id = id
        self._dy = 0
        self._point = 0
        self.input = [0, 0]
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self):
        return self._id

    def get_point(self):
        return self._point

    def set_point(self, value):
        self._point = value

    # set to player id if player won the last point
    point = property(get_point, set_point)

    def get_speed(self):
        return self._speed

    def set_speed(self, value):
        self._speed = value

    speed = property(get_speed, set_speed)

    def get_score(self):
        return self._score

    def set_score(self, value):
        self._score = value

    score = property(get_score, set_score)

    def get_dy(self):
        return self._dy

    def set_dy(self, v):
        self._dy = sign(v)

    dy = property(get_dy, set_dy)

    # update the paddle position
    def update(self, dt: float, sprites: arcade.SpriteList):
        touched = arcade.check_for_collision_with_list(self, sprites)
        if touched:
            if touched[0].name == "top":
                self.dy = -1 if self.input[1] else 0
            elif touched[0].name == "bottom":
                self.dy = 1 if self.input[0] else 0
        else:
            if self.input[0] == 1:
                self.dy = 1
            elif self.input[1] == 1:
                self.dy = -1
            else:
                self.dy = 0

        self.center_y += self.speed * dt * self.dy

    # set the movement condition
    def move(self, key, d):
        self.input[key] = d

    # ai logic to control paddle
    def track(self, ball, edge):
        if (self.id == 1 and ball.dx == -1) or (self.id == 2 and ball.dx == 1):
            # get the difference between the center points
            delta = ball.center_y - self.center_y
            if math.fabs(delta) > 10.5:
                self.dy = sign(delta) * -1
            else:
                self.dy = 0
            return
        if math.fabs(self.center_y - edge.center_y) > 10.5:
            self.dy = sign(self.center_y - edge.center_y) * -1
        else:
            self.dy = 0
        return
