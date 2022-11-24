import arcade
import const
from gameData import gameData
from start_view import StartView
from serve_view import ServeView
from game_view import GameView
from game_over_view import GameOver


def main():
    """ Main method """
    # create the primary window and the game data
    gd = gameData()
    #initiallize the views
    gd.start_view = StartView(gd)
    gd.serve_view = ServeView(gd)
    gd.game_view = GameView(gd)
    gd.game_over_view = GameOver(gd)
    # display the initial view
    gd.next('start')
    # run the aplication
    arcade.run()


if __name__ == "__main__":
    main()
