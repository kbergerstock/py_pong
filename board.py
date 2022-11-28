import const
import random as rand
import arcade
from arcade import color
from fps import FPS
from ball import BallSprite
from paddle import Paddle
from const import EDGES

SCORE_MARGIN = 40
EDGE_MARGIN = 12
TOP_MARGIN = SCORE_MARGIN + EDGE_MARGIN
EDGE_LINE_WIDTH = 8
END_MARGIN = 12


class Board(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.edges = None
        # condition the random generator
        rand.seed()
        for i in range(8):
            rand.randrange(25, 85)
        self.window = window
        self.create_board()
        self.fps = FPS()
        self.ball = BallSprite()
        self.player1 = Paddle(1)
        self.player2 = Paddle(2)
        self.home_paddle(1)
        self.home_paddle(2)
        self.actions = arcade.SpriteList()
        self.actions.append(self.player1)
        self.actions.append(self.player2)
        self.actions.append(self.ball)
        self.AIplayer_1 = False
        self.AIplayer_2 = False

    def get_edge(self):
        return self.repeat_count_x

    def set_edge(self, v):
        self.reapeat_count_x = v

    edge = property(get_edge, set_edge)

    def xw(self, margin):
        return self.window.width - margin

    def xh(self, margin):
        return self.window.height - margin

    # the edges are stored in this oreder
    # top 0
    # bottom 1
    # player1 2
    # player2 3

    def home_paddle(self, id):
        if id == 1:
            self.player1.center_x = self.edges[2].center_x + 20
            self.player1.center_y = self.edges[1].center_y + 50
        else:
            self.player2.center_x = self.edges[3].center_x - 20
            self.player2.center_y = self.edges[0].center_y - 50

    def create_board(self):
        self.edges = arcade.SpriteList(True)
        top = arcade.SpriteSolidColor(
            self.xw(END_MARGIN), EDGE_LINE_WIDTH, color.ALICE_BLUE
        )
        top.center_x = self.window.width // 2
        top.center_y = self.window.height - TOP_MARGIN
        top.edge = EDGES["top"]
        self.edges.append(top)
        bot = arcade.SpriteSolidColor(
            self.xw(END_MARGIN), EDGE_LINE_WIDTH, color.AERO_BLUE
        )
        bot.center_x = top.center_x
        bot.center_y = EDGE_MARGIN
        bot.edge = EDGES["bottom"]
        self.edges.append(bot)
        eh = top.center_y - bot.center_y - EDGE_LINE_WIDTH
        ecy = EDGE_MARGIN + (top.center_y - bot.center_y) / 2.0
        end1 = arcade.SpriteSolidColor(EDGE_LINE_WIDTH, eh, color.ALIZARIN_CRIMSON)
        end1.center_x = END_MARGIN
        end1.center_y = ecy
        end1.edge = EDGES["player1"]
        self.edges.append(end1)
        end2 = arcade.SpriteSolidColor(EDGE_LINE_WIDTH, eh, color.ALIZARIN_CRIMSON)
        end2.center_x = self.window.width - END_MARGIN
        end2.center_y = ecy
        end2.edge = EDGES["player2"]
        self.edges.append(end2)

    def on_draw(self):
        arcade.start_render()
        self.render_fps()
        self.render_velocity()
        self.render_score()
        self.edges.draw()
        self.actions.draw()

    def on_update(self, delta_time):
        self.fps.update(delta_time)
        self.player1.update(delta_time, self.edges)
        self.player2.update(delta_time, self.edges)
        self.ball.update(delta_time, self.edges, [self.player1, self.player2])
        if self.AIplayer_1:
            self.player1.track(self.ball, self.edges)
        if self.AIplayer_2:
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
        if key_code == 97 and not self.AIplayer_1:
            self.player1.move(1, 0)  # stop the down movement
            self.player1.move(0, 1)  # start the up movement
        # key code for 'd'
        elif key_code == 100 and not self.AIplayer_1:
            self.player1.move(0, 0)  # stop the up movment
            self.player1.move(1, 1)  # start the down movement
        # key code for 'left'
        elif key_code == 65361 and not self.AIplayer_2:
            self.player2.move(1, 0)
            self.player2.move(0, 1)
        # key code for 'right'
        elif key_code == 65363 and not self.AIplayer_2:
            self.player2.move(0, 0)
            self.player2.move(1, 1)
        elif key_code == 32:
            self.ball.dx = rand.choice([1, -1])
            self.ball.dy = rand.choice([1, -1])
        elif key_code == 49:
            self.AIplayer_1 = not self.AIplayer_1
        elif key_code == 50:
            self.AIplayer_2 = not self.AIplayer_2

    def on_key_release(self, key_code, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # stop the motion that coresponds to the key code
        if key_code == 97 and not self.AIplayer_1:
            self.player1.move(0, 0)

        elif key_code == 100 and not self.AIplayer_1:
            self.player1.move(1, 0)

        elif key_code == 65361 and not self.AIplayer_2:
            self.player2.move(0, 0)

        elif key_code == 65363 and not self.AIplayer_2:
            self.player2.move(1, 0)
            
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_press(x, y, button, modifiers)
        pass

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
