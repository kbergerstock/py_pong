import arcade
from arcade import color


__TEXTURES = {"QTY": 1}


def create_texture(w, h, _color):
    if _color[0] in __TEXTURES:
        _texture = __TEXTURES[_color[0]]
    else:
        _texture = arcade.Texture.create_filled(_color[0], (w, h), _color[1])
        __TEXTURES[_color[0]] = _texture
    return _texture


def main():
    t0 = create_texture(50, 30, ["GREY", color.ASH_GREY])
    t1 = create_texture(50, 30, ["ANDROID_GREEN", color.ANDROID_GREEN])
    print(type(t0))
    print(t0)
    print(t0.name)
    print(type(t1))
    print(t1)
    print(t1.name)


if __name__ == "__main__":
    main()
