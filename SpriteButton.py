# spriteButton.py
# keith.bergerstock
# 11/28.2022

import math
import arcade
from arcade import color
from create_texture import create_texture


class SpriteButton(arcade.SpriteSolidColor):
    def __init__(
        self,
        x,
        y,
        w=60,
        h=20,
        colors=[["ORANGE", color.ORANGE], ["BRIGHT_GREEN", color.BRIGHT_GREEN]],
    ):
        super().__init__(w, h, colors[0][1])
        self.textures.append(create_texture(w, h, colors[0]))
        self.textures.append(create_texture(w, h, colors[1]))
        self.status = False
        self.set_position(x, y)

    def get_state(self) -> bool:
        return self._state

    def set_state(self, state: bool):
        self._state = state
        self.set_texture(state)

    status = property(get_state, set_state)
