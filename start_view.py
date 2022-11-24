# starting view

import arcade
from arcade import color
import const
import gameData
from ball import FPS
from ball import BALL
from ball import PADDLE
from serve_view import ServeView

def draw_msg(msg,x,y,color,size):
    arcade.draw_text(msg,x,y,color,width=const.MSG_WIDTH,align='center',font_size=size,font_name=const.GAME_FONT)


class StartView(arcade.View):
    def __init__(self,gd):
        """ This is run once when we switch to this view """
        super().__init__()
        self.gd = gd

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(const.SCREEN_COLOR)
        self.gd.AIplayer_1 = False
        self.gd.AIplayer_2 = False        

    def on_draw(self):
        """ render the view """
        arcade.start_render()
        if self.gd == None:
            arcade.draw_text("game data uninitialized",20,500,color.RED,align='center',font_size=50)
        else:    
            self.gd.fps.render(5,5,color.ANDROID_GREEN,const.GAME_FONT)
            msg = 'WELCOME to PONG'
            arcade.draw_msg(msg,20,600,color.ANDROID_GREEN,32)
            if self.gd.AIplayer_1: msg = 'Press 1 for user player one'
            else : msg = 'Press 1 for compter player one'
            arcade.draw_msg(msg,20,560,color.ARMY_GREEN,20)
            if self.gd.AIplayer_2: msg = 'Press 2 for user player two'
            else : msg = 'Press 2 for compter player two'
            arcade.draw_msg(msg,20,535,color.ARMY_GREEN,20)
            msg = 'Press SpaceBar to begin!'
            arcade.draw_msg(msg,20,510,color.ARMY_GREEN,20)

    def on_key_press(self, key_code, key_modifiers):
        """ process event signals """
        if key_code == 49:
            self.gd.AIplayer_1 = not self.gd.AIplayer_1

        elif key_code == 50:
            self.gd.AIplayer_2 = not self.gd.AIplayer_2

        elif key_code == 32: 
            self.gd.next('serve')
