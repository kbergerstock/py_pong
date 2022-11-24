# gameData.py
import const
import arcade
from arcade import color
from ball import FPS
from ball import BALL
from ball import PADDLE
from start_view import startView
from serve_view import serveView
from game_view import gameView
from game_over_view import GameOver


class gameData:
    def __init__(self):
        self.window = arcade.Window(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, const.SCREEN_TITLE)
        self.window.center()
        self.AIplayer_1 = False
        self.AIplayer_2 = False
        self.point = False
        self.id = 1
        self.player_1 = PADDLE(1)
        self.player_2 = PADDLE(2)
        self.ball = BALL()
        self.fps = FPS()
        self.start_view = startView(self)
        self.serve_view = serveView(self)
        self.game_view = gameView(self)
        self.game_over_view = GameOver(self)

    def renderScore(self):
        s1 = self.player_1.getScore()
        s2 = self.player_2.getScore()
        msg = f" {s1} : {s2}"
        arcade.draw_text(
            msg,
            0,
            600,
            color.ANDROID_GREEN,
            width=const.SCREEN_WIDTH,
            align="center",
            font_size=50,
            font_name=const.GAME_FONT,
        )
        
    def next(self,szNext):
        if szNext == 'serve':
            view = self.serve_view
        elif szNext == 'game':
            view = self.game_view
        elif szNext == 'over':
            view = self.game_over_view
        else:
            view = self.start_view    
        self.window.show_view(view)    
