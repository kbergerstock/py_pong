import const
import random as rand
import arcade
from arcade import color
from fps import FPS
from ball import BallSprite
from paddle import Paddle
from const import EDGES
from SpriteButton import SpriteButton as Toggle

SCORE_MARGIN = 40
EDGE_MARGIN = 12
TOP_MARGIN = SCORE_MARGIN + EDGE_MARGIN
EDGE_LINE_WIDTH = 15


class Board(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.edges = None
        self.fps = FPS()
        # condition the random generator
        rand.seed()
        for i in range(8):
            rand.randrange(25, 85)
        self.window = window
        self.create_board()
        # create the movable ubjects
        self.ball = BallSprite()
        self.player1 = Paddle(1)
        self.player2 = Paddle(2)
        self.home()
        # set up a sprite list to draw all moveable objects
        self.actions = arcade.SpriteList()
        self.actions.append(self.player1)
        self.actions.append(self.player2)
        self.actions.append(self.ball)
        self.AIplayer_1 = Toggle(35, window.height - 25)
        self.AIplayer_2 = Toggle(100, window.height - 25)
        k = [["RED", color.RED], ["GREEN", color.GREEN]]
        self.led1 = Toggle(400, window.height - 25, w=20, h=20, colors=k)
        self.led2 = Toggle(window.width - 400, window.height - 25, w=20, h=20, colors=k)
        self.buttons = arcade.SpriteList()
        self.buttons.append(self.AIplayer_1)
        self.buttons.append(self.AIplayer_2)
        self.buttons.append(self.led1)
        self.buttons.append(self.led2)
        self.serve = rand.choice([1, 2])
        self.set_server(self.serve)

    def get_edge(self):
        return self.repeat_count_x

    def set_edge(self, v):
        self.reapeat_count_x = v

    edge = property(get_edge, set_edge)

    # the edges are stored in this oreder
    # top 0
    # bottom 1
    # player1 2
    # player2 3

    def home(self):
        self.player1.center_x = (
            self.edges[2].center_x + 5 + (EDGE_LINE_WIDTH + self.player1.width) / 2
        )
        self.player1.center_y = (
            self.edges[1].center_y + 5 + (EDGE_LINE_WIDTH + self.player1.height) / 2
        )
        self.player2.center_x = (
            self.edges[3].center_x - 5 - (EDGE_LINE_WIDTH + self.player2.width) / 2
        )
        self.player2.center_y = (
            self.edges[0].center_y - 5 - (EDGE_LINE_WIDTH + self.player2.height) / 2
        )

    def create_board(self):
        self.edges = arcade.SpriteList(True)
        LW = self.window.width - 2 * EDGE_MARGIN - EDGE_LINE_WIDTH
        top = arcade.SpriteSolidColor(LW, EDGE_LINE_WIDTH, color.ALICE_BLUE)
        top.center_x = self.window.width // 2
        top.center_y = self.window.height - TOP_MARGIN
        top.edge = EDGES["top"]
        self.edges.append(top)
        bot = arcade.SpriteSolidColor(LW, EDGE_LINE_WIDTH, color.AERO_BLUE)
        bot.center_x = top.center_x
        bot.center_y = EDGE_MARGIN
        bot.edge = EDGES["bottom"]
        self.edges.append(bot)
        eh = top.center_y - bot.center_y + EDGE_LINE_WIDTH
        ecy = EDGE_MARGIN + (top.center_y - bot.center_y) / 2.0
        end1 = arcade.SpriteSolidColor(EDGE_LINE_WIDTH, eh, color.ALIZARIN_CRIMSON)
        end1.center_x = EDGE_MARGIN + EDGE_LINE_WIDTH / 2
        end1.center_y = ecy
        end1.edge = EDGES["player1"]
        self.edges.append(end1)
        end2 = arcade.SpriteSolidColor(EDGE_LINE_WIDTH, eh, color.ALIZARIN_CRIMSON)
        end2.center_x = self.window.width - EDGE_MARGIN - EDGE_LINE_WIDTH / 2
        end2.center_y = ecy
        end2.edge = EDGES["player2"]
        self.edges.append(end2)

    def on_draw(self):
        arcade.start_render()
        self.render_fps()
        self.render_velocity()
        self.render_score()
        self.buttons.draw()
        self.edges.draw()
        self.actions.draw()

    def set_server(self, player_id):
        self.serve = player_id
        # id = 1 maps to buttons[2]
        # id = 2 maps to buttons[3]
        # 5 - idx maps to the opposite led
        idx = player_id + 1
        self.buttons[idx].status = True
        self.buttons[5 - idx].status = False

    def score(self):
        if self.player1.point:
            player = self.player1
        else:
            player = self.player2

        if player.point and self.serve == player.id:
            player.score += 1
        else:
            self.set_server(player.id)

        if self.AIplayer_1.status and self.AIplayer_2.status:
            self.ball.speed = const.BALL_VELOCITY
            self.ball.dx = 1 if self.serve == 1 else -1
            self.ball.dy = rand.choice([1, -1])

    def on_update(self, delta_time):
        self.fps.update(delta_time)
        self.player1.update(delta_time, self.edges)
        self.player2.update(delta_time, self.edges)
        # ball update returns True when it is out of bounds
        if self.ball.update(delta_time, self.edges, [self.player1, self.player2]):
            self.score()
        if self.AIplayer_1.status:
            self.player1.track(self.ball, self.edges)
        if self.AIplayer_2.status:
            self.player2.track(self.ball, self.edges)

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
        if key_code == 97 and not self.AIplayer_1.status:
            self.player1.move(1, 0)  # stop the down movement
            self.player1.move(0, 1)  # start the up movement
        # key code for 'd'
        elif key_code == 100 and not self.AIplayer_1.status:
            self.player1.move(0, 0)  # stop the up movment
            self.player1.move(1, 1)  # start the down movement
        # key code for 'left'
        elif key_code == 65361 and not self.AIplayer_2.status:
            self.player2.move(1, 0)
            self.player2.move(0, 1)
        # key code for 'right'
        elif key_code == 65363 and not self.AIplayer_2.status:
            self.player2.move(0, 0)
            self.player2.move(1, 1)
        elif key_code == 32:
            self.ball.speed = const.BALL_VELOCITY
            self.ball.dx = 1 if self.serve == 1 else -1
            self.ball.dy = rand.choice([1, -1])
        elif key_code == 49:
            self.AIplayer_1.status = not self.AIplayer_1.status
        elif key_code == 50:
            self.AIplayer_2.status = not self.AIplayer_2.status

    def on_key_release(self, key_code, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # stop the motion that coresponds to the key code
        if key_code == 97 and not self.AIplayer_1.status:
            self.player1.move(0, 0)

        elif key_code == 100 and not self.AIplayer_1.status:
            self.player1.move(1, 0)

        elif key_code == 65361 and not self.AIplayer_2.status:
            self.player2.move(0, 0)

        elif key_code == 65363 and not self.AIplayer_2.status:
            self.player2.move(1, 0)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        tb = arcade.get_sprites_at_point((x, y), self.buttons)
        if tb:
            tb[0].status = not tb[0].status
        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_release(x, y, button, modifiers)
        pass


def main():
    window = arcade.Window(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    window.center_window()
    board = Board(window)
    window.show_view(board)
    arcade.run()


if __name__ == "__main__":
    main()
