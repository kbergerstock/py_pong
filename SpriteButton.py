# spriteButton.py
# keith.bergerstock
# 11/28.2022

import arcade
from arcade import color

from create_texture import create_texture


class SpriteButton(arcade.BasicSprite):
    def __init__(
        self,
        x: float,
        y: float,
        w=60,
        h=20,
        colors=[["ORANGE", color.ORANGE], ["BRIGHT_GREEN", color.BRIGHT_GREEN]],
        name="NA",
    ):
        super().__init__(create_texture(w, h, colors[0][1]))
        self.textures = {
            1: 1,
            2: 22,
        }
        self.center_x = x
        self.center_y = y
        self._colors = colors
        self._track = False
        self._serve = False
        self._name = name
        self.textures[1] = create_texture(w, h, colors[0])
        self.textures[2] = create_texture(w, h, colors[1])

    @property
    def name(self) -> str:
        return self._name

    def track_get(self) -> bool:
        return self._track

    def track_set(self, value: bool):
        self._track = value

    track = property(track_get, track_set)

    def update_led(self, server: int):
        self.texture = self.textures[server]
