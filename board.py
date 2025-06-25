import const
import random as rand
import arcade
from arcade import color
from fps import FPS
from ball import BallSprite
from paddle import Paddle
from const import EDGE
from SpriteButton import SpriteButton as Toggle
from edge import Edge
from icecream import ic

SCORE_MARGIN = 40
EDGE_MARGIN = 12
TOP_MARGIN = SCORE_MARGIN + EDGE_MARGIN
EDGE_LINE_WIDTH = 15


class Board(arcade.View):
    def __init__(self, window):
        super().__init__()
        # declare the sprit list for the application
        self.sprites = arcade.SpriteList(True)
        self.fps = FPS()
        # condition the random generator
        rand.seed()
        for i in range(8):
            rand.randrange(25, 85)
        self.window = window
        self.create_board()
        # create the movable objects
        self.ball = BallSprite("ball")
        self.player1 = Paddle(1, name="ply1")
        self.player2 = Paddle(2, k=["RED", color.ALIZARIN_CRIMSON], name="ply2")
        # set up a sprite list to draw all moveable objects
        self.sprites.append(self.player1)
        self.sprites.append(self.player2)
        self.sprites.append(self.ball)
        self.AIplayer_1 = Toggle(35, window.height - 25, name="AI1")
        self.AIplayer_2 = Toggle(100, window.height - 25, name="AI2")
        k = [["RED", color.RED], ["GREEN", color.GREEN]]
        self.led1 = Toggle(400, window.height - 25, w=20, h=20, colors=k, name="led1")
        self.led2 = Toggle(window.width - 400, window.height - 25, w=20, h=20, colors=k, name="led2")
        self.sprites.append(self.AIplayer_1)
        self.sprites.append(self.AIplayer_2)
        self.sprites.append(self.led1)
        self.sprites.append(self.led2)
        self.home(self.sprites)
        # keep track of who is server
        self._server = 0
        # flow control booleans
        self.wait_for_serve = True
        self.game_started = False
        self.game_over = True
        self.check_score = False
        self.enter_initials = False
        self.auto_play = False
        self.wait_for_auto_serve = False
        self.about_flag = False

    # the self.sprites are stored in this order
    # top 0
    # bottom 1
    # player1 2
    # player2 3

    def home(self, edges):
        self.player1.center_x = edges[EDGE["end1"]].center_x + 5 + (EDGE_LINE_WIDTH + self.player1.width) // 2
        self.player1.center_y = edges[EDGE["bottom"]].center_y + 5 + (EDGE_LINE_WIDTH + self.player1.height) // 2
        self.player2.center_x = edges[EDGE["end2"]].center_x - 5 - (EDGE_LINE_WIDTH + self.player2.width) // 2
        self.player2.center_y = edges[EDGE["top"]].center_y - 5 - (EDGE_LINE_WIDTH + self.player2.height) // 2

    def create_board(self):
        """create the board using sprites
        to enable sprite detection for boundry checks
        append the sprites to the sprite list
        """
        LW = self.window.width - 2 * EDGE_MARGIN - EDGE_LINE_WIDTH
        top = Edge(LW, EDGE_LINE_WIDTH, color.ALICE_BLUE, name="top")
        top.center_x = self.window.width // 2
        top.center_y = self.window.height - TOP_MARGIN
        self.sprites.append(top)
        bot = Edge(LW, EDGE_LINE_WIDTH, color.AERO_BLUE, name="bottom")
        bot.center_x = self.window.width // 2
        bot.center_y = EDGE_MARGIN
        self.sprites.append(bot)
        eh = top.center_y - bot.center_y + EDGE_LINE_WIDTH
        ecy = EDGE_MARGIN + (top.center_y - bot.center_y) // 2
        end1 = Edge(EDGE_LINE_WIDTH, eh, color.ALIZARIN_CRIMSON, name="end1")
        end1.center_x = EDGE_MARGIN + EDGE_LINE_WIDTH // 2
        end1.center_y = ecy
        self.sprites.append(end1)
        end2 = Edge(EDGE_LINE_WIDTH, eh, color.ALIZARIN_CRIMSON, name="end2")
        end2.center_x = self.window.width - EDGE_MARGIN - EDGE_LINE_WIDTH // 2
        end2.center_y = ecy
        self.sprites.append(end2)

    def on_draw(self):
        self.clear()
        self.sprites.draw()
        self.render_fps()
        self.render_velocity()
        self.render_score()

    def score(self, v, name):
        if v and (name == "ply1" or name == "ply2"):
            player = self.sprites[EDGE[name]]
            if player.point:
                player.score += 1
            else:
                # change sever side if no point was mde
                self._server = 2 if player.id == 1 else 2

            ic(name, v, player.name, player.id, player.point, self._server)
            # FIX does not belong here
            if self.AIplayer_1.track and self.AIplayer_2.track:
                self.ball.speed = const.BALL_VELOCITY
                self.ball.dx = 1 if self._server else -1
                self.ball.dy = rand.choice([1, -1])

    def on_update(self, delta_time):
        if self.wait_for_auto_serve:
            self.fps.update(delta_time)
        else:
            self.player1.update(delta_time, self.sprites)
            self.player2.update(delta_time, self.sprites)
            self.led1.update_led(self.server)
            self.led2.update_led(self._server)
            # ball update returns True when it is out of bounds
            self.score(*self.ball.update(delta_time, self.sprites, self._server))
            if self.auto_play and self.AIplayer_1.track:
                self.player1.track(self.ball, self.sprites[EDGE["end1"]])
            if self.auto_play and self.AIplayer_2.track:
                self.player2.track(self.ball, self.sprites[EDGE["end2"]])

    def render_fps(self):
        arcade.draw_text(
            "FPS {0:02}".format(self.fps.fps),
            self.window.width - 190,
            self.window.height - 20,
            color.AMBER,
            font_size=12,
            font_name=const.GAME_FONT[1],
        )

    def render_velocity(self):
        arcade.draw_text(
            "Velocity {0:04.2f} ".format(self.ball.speed),
            self.window.width - 125,
            self.window.height - 20,
            color.AMBER,
            font_size=12,
            font_name=const.GAME_FONT[0],
        )

    def render_score(self):
        arcade.draw_text(
            " {0} : {1}".format(self.player1.score, self.player2.score),
            0,
            self.window.height - 40,
            color.ANDROID_GREEN,
            width=self.window.width,
            align="center",
            font_size=32,
            font_name=const.GAME_FONT,
        )

    def on_key_press(self, key_code, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        # key code for 'a'
        if key_code == 97 and not self.AIplayer_1.track:
            self.player1.move(1, 0)  # stop the down movement
            self.player1.move(0, 1)  # start the up movement
        # key code for 'd'
        elif key_code == 100 and not self.AIplayer_1.track:
            self.player1.move(0, 0)  # stop the up movement
            self.player1.move(1, 1)  # start the down movement
        # key code for 'left'
        elif key_code == 65361 and not self.AIplayer_2.track:
            self.player2.move(1, 0)
            self.player2.move(0, 1)
        # key code for 'right'
        elif key_code == 65363 and not self.AIplayer_2.track:
            self.player2.move(0, 0)
            self.player2.move(1, 1)
        elif key_code == 32:
            if not self.game_started:
                self._server = rand.choice([1, 2])
                self.game_started = True
            self.ball.speed = const.BALL_VELOCITY
            self.ball.dx = 1 if self._server == 1 else -1
            self.ball.set_angle()
            self.ball.dy = rand.choice([1, -1])
        elif key_code == 49:
            self.AIplayer_1.track = not self.AIplayer_1.track
        elif key_code == 50:
            self.AIplayer_2.track = not self.AIplayer_2.track

    def on_key_release(self, key_code, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # stop the motion that corresponds to the key code
        if key_code == 97 and not self.AIplayer_1.track:
            self.player1.move(0, 0)

        elif key_code == 100 and not self.AIplayer_1.track:
            self.player1.move(1, 0)

        elif key_code == 65361 and not self.AIplayer_2.track:
            self.player2.move(0, 0)

        elif key_code == 65363 and not self.AIplayer_2.track:
            self.player2.move(1, 0)

    # FIX THIS MODULE
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        tb = arcade.get_sprites_at_point((x, y), self.sprites)
        if tb:
            tb[0].status = not tb[0].status
        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_release(x, y, button, modifiers)
        pass
