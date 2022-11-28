# ball.py
# k.r.bergerstock junr 2020
# object classes for pong.py
import math
import arcade
from arcade import color
from const import sign
from const import EDGES


class Paddle(arcade.SpriteSolidColor):
    __SPEED = 500

    def __init__(self, id):
        super().__init__(18, 75, color.PARIS_GREEN)
        self._speed = Paddle.__SPEED
        self._score = 0
        self._id = id
        self._dy = 0
        self._track = 0
        self._point = 0
        self.input = [0, 0]

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

    @property
    def id(self):
        return self._id

    def get_dy(self):
        return self._dy

    def set_dy(self, v):
        self._dy = sign(v)

    dy = property(get_dy, set_dy)

    # update the paddle position
    def update(self, dt: float, edges):
        # check boundries
        touched = arcade.check_for_collision_with_list(self, edges)
        if touched:
            edge = touched[0].edge
            if (edge == EDGES["top"] and self.dy == 1) or (
                edge == EDGES["bottom"] and self.dy == -1
            ):
                self.dy = 0
        # move
        self.center_y += self.speed * dt * self.dy

    # set the movement condition
    def move(self, key, d):
        self.input[key] = d
        # move 1 pixel at a time
        if self.input[0] == 1:
            self.dy = 1
        elif self.input[1] == 1:
            self.dy = -1
        else:
            self.dy = 0

    # ai logic to control paddle
    def track(self, sprite, edges):
        if (self.id == 1 and sprite.dx == -1) or (self.id == 2 and sprite.dx == 1):
            # get the difference betwwen the center points
            if math.fabs(sprite.center_y - self.center_y) > 10.5:
                self.dy = sign(self.center_y - sprite.center_y) * -1
            else:
                self.dy = 0
        elif math.fabs(self.center_y - edges[2].center_y) > 10.5:
            self.dy = sign(self.center_y - edges[2].center_y) * -1
        else:
            self.dy = 0
