# ball.py
# k.r.bergerstock junr 2020
# object classes for pong.py
import const
import arcade
from arcade import color
from const import sign


class Paddle(arcade.SpriteSolidColor):
    __SPEED = 500

    def __init__(self, id):
        super().__init__(18, 75, color.PARIS_GREEN)
        self._speed = Paddle.__SPEED
        self._score = 0
        self._id = id
        self._dy = 0
        self.home()
        self.input = [0, 0]

    def home(self):
        if self.id == 1:
            self.set_position(30, 60)
        else:
            self.set_position(const.SCREEN_WIDTH - 30, const.SCREEN_HEIGHT - 60)

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

    def reset(self):
        self.dy = 0
        self.input[0] = 0
        self.input[1] = 0

    def scored(self):
        self.score += 1

    # update the paddle position
    def update(self, dt, edges):
        # check boundries
        if self.dy != 0:
            touched = arcade.check_for_collision_with_list(self,edges)
            if not touched:
                self.center_y += self.dy * self.speed * dt
            else    :
                self.center_y = touched[0].center_y + (4 + (touched[0].height + self.height) // 2) * self.dy * -1
                self.dy = 0

    # set the movement condition
    def move(self, key, d):
        self.input[key] = d
        # move 1 virtual pixel at a time
        if self.input[0] == 1:
            self.dy = 1
        elif self.input[1] == 1:
            self.dy = -1
        else:
            self.dy = 0

    # ai logic to control paddle
    def track(self, sprite):
        # get the difference betwwen the center points
        self.dy = sign(sprite.center_y - self.center_y)

    def render(self):
        self.draw()
