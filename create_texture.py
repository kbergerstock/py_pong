import arcade
from arcade import BasicSprite, color
from icecream import ic as IC

__TEXTURES = {"QTY": 1}


def create_texture(w, h, _color=("GREY", color.ASH_GREY)):
    if _color[0] in __TEXTURES:
        _texture = __TEXTURES(_color[0])
    else:
        _texture = arcade.Texture.create_empty(_color[0], (w, h), _color[1])
    return _texture


def main():
    t0 = create_texture(1, 1, ("GREY", color.ASH_GREY))
    t1 = create_texture(50, 30, ("ANDROID_GREEN", color.ANDROID_GREEN))
    t2 = create_texture(50, 30, ("GREY", color.ASH_GREY))
    t3 = create_texture(5, 5, ("RED", color.ALABAMA_CRIMSON))
    t4 = create_texture(10, 10, ("ANDROID_GREEN", color.ANDROID_GREEN))
    t5 = BasicSprite(t0)
    IC(type(t0))
    IC(t0, t0._cache_name, t0._size)
    IC(type(t1))
    IC(t1, t1._cache_name, t1.size)
    IC(type(t2))
    IC(t2, t2._cache_name, t2._size)
    IC(type(t3))
    IC(t3, t3._cache_name, t3._size)
    IC(type(t4))
    IC(t4, t4._cache_name, t4._size)
    IC(type(t5))
    IC(t5)
    IC(t5.size, t5.texture.size)
    IC(t5.color, t5.texture)
    t5.texture = t1
    IC(t5.size, t5.texture.size)
    IC(t5.color, t5.texture)
    t5.texture = t2
    IC(t5.size, t5.texture.size)
    IC(t5.color, t5.texture)
    t5.texture = t2
    IC(t5.size, t5.texture.size)
    IC(t5.color, t5.texture)
    t5.texture = t2
    IC(t5.size, t5.texture.size)
    IC(t5.color, t5.texture)


if __name__ == "__main__":
    main()
