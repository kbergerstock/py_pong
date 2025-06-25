# pong constants

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
MSG_WIDTH = SCREEN_WIDTH - 40
SCREEN_TITLE = "PONG"
SCREEN_COLOR = [40, 45, 52, 1]
EDGE = {"top": 0, "bottom": 1, "end1": 2, "end2": 3, "ply1": 4, "ply2": 5}

BALL_VELOCITY = 500

GAME_FONT = ("RETRO_FONT", "ATARI", "Terminal")


def sign(v) -> float:
    return 1.0 if v > 0 else (-1.0 if v < 0 else 0.0)
