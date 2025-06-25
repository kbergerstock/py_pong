# version 2.0
# updated to be compatible with python 3.13.3 and arcade 3.4.2
# k.r.bergerstock @ 05/2025

import const
import arcade
from board import Board


def main():
    window = arcade.Window(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    window.center_window()
    board = Board(window)
    window.show_view(board)
    arcade.run()


if __name__ == "__main__":
    main()
