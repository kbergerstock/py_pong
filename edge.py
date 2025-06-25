import arcade
from arcade import color


class Edge(arcade.SpriteSolidColor):
    def __init__(self, width: int, height: int, shade: color, name="unk"):
        super().__init__(width, height, shade)
        self._name = name

    @property
    def name(self) -> str:
        return self._name
