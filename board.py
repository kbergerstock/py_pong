import const
import random as rand
import arcade
from arcade import color
from fps import FPS
from ball import BallSprite
from paddle import Paddle


class Board(arcade.View):
    EDGES = {"top": 10, "bottom": 11, "player1": 20, "player2": 21}

    def __init__(self):
        super().__init__()
        # condition the random generator
        rand.seed()
        for i in range(8):
            rand.randrange(25, 85)
        self.create_board()
        self.fps = FPS()
        self.ball = BallSprite()
        self.player1 = Paddle(1)
        self.player2 = Paddle(2)
        self.actions = arcade.SpriteList()
        self.actions.append(self.player1)
        self.actions.append(self.player2)
        self.actions.append( self.ball)
        self.AIplayer_1 = False
        self.AIplayer_2 = False        

    def get_edge(self):
        return self.repeat_count_x

    def set_edge(self, v):
        self.reapeat_count_x = v

    edge = property(get_edge, set_edge)

    def create_board(self):
        self.edges = arcade.SpriteList(True)
        top = arcade.SpriteSolidColor(const.SCREEN_WIDTH - 16, 8, color.ALICE_BLUE)
        top.center_x = const.SCREEN_WIDTH // 2
        top.center_y = const.SCREEN_HEIGHT - 12
        top.edge = Board.EDGES["top"]
        self.edges.append(top)
        bot = arcade.SpriteSolidColor(const.SCREEN_WIDTH - 16, 8, color.AERO_BLUE)
        bot.center_x = const.SCREEN_WIDTH // 2
        bot.center_y = 12
        bot.edge = Board.EDGES["bottom"]
        self.edges.append(bot)
        end1 = arcade.SpriteSolidColor(
            8, const.SCREEN_HEIGHT - 32, color.ALIZARIN_CRIMSON
        )
        end1.center_x = 12
        end1.center_y = const.SCREEN_HEIGHT // 2
        end1.edge = Board.EDGES["player1"]
        self.edges.append(end1)
        end2 = arcade.SpriteSolidColor(
            8, const.SCREEN_HEIGHT - 32, color.ALIZARIN_CRIMSON
        )
        end2.center_x = const.SCREEN_WIDTH - 12
        end2.center_y = const.SCREEN_HEIGHT // 2
        end2.edge = Board.EDGES["player2"]
        self.edges.append(end2)

    def on_draw(self):
        arcade.start_render()
        self.render_fps()
        self.edges.draw()
        self.actions.draw()


    def on_update(self, delta_time):
        self.fps.update(delta_time)
        self.player1.update(delta_time, self.edges)
        self.player2.update(delta_time, self.edges)
        self.ball.update(delta_time)

    def render_fps(self):
        arcade.draw_text(
            "{0:03}".format(self.fps.fps),
            120,
            30,
            color.AMBER,
            font_size=12,
            font_name=const.GAME_FONT[1],
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


def main():
    window = arcade.Window(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    board = Board()
    window.show_view(board)
    arcade.run()


if __name__ == "__main__":
    main()
