# Colors
WHITE   = (255, 255,255)
BLUE    = (0,   0,  255)
RED     = (255, 0,  0)
BLACK   = (0,   0,  0)

#       display
FPS = 60  # calc speed as well
RESOLUTION = (1000, 800)
WIDTH = RESOLUTION[0]
HEIGHT = RESOLUTION[1]
FULLSCREEN = False
TANK_LAYER = 3
BULLET_LAYER = 2
WALL_LAYER = 4
BG_LAYER = 0
POW_LAYER = 1
EXPLOSION_LAYER = 4
FONT_NAME = "Times"
BG_COLOR = WHITE
NAME = "Tank Game"

EXPL1 = "boom3.png"
FRAME_TICK_RATES_EXPL = 70

# graphics
TANK_IMG_DIC =\
    {"red":  [(588, 0, 83, 78), (834, 0, 24, 58)],\
    "blue": [(506, 78, 83, 78),(827, 226, 24,58)]}
BULLET_IMG_DIC =\
    {"normal":{"red":(711, 140, 20, 34), "blue":(148, 345, 20, 34)},\
    "berta":{"red":(735, 300, 20, 34), "blue":(755, 300, 20, 34)}}
EXPLOSION_IMG_DICT =\
    {"white":[(324, 107, 92, 89),\
              (396, 285, 90, 99),\
              (590, 182, 79, 79),\
              (128, 0, 100, 97),\
              (226, 194, 98, 107),\
              (418, 0, 87, 87)]}
BG_IMG_DICT = {"grass":(0, 128, 128, 128), "dirt":(0, 0, 128, 128), "sand":(0, 256, 128, 128)}
BG_ATM = "grass"

# game stats
WALLS_NUMBER = 0

# music
MUSIC_VOL_INGAME = 0 # 0.2 is good
MUSIC_VOL_LS = 0   # 1.4 is good

# tank
TANK_SPEED = 200 / FPS
TURN_SPEED = 120 / FPS
TANK_GEAR = {0: 0,
             1: TANK_SPEED,
             -1: -TANK_SPEED}
TANK_START_POS = {"red": (RESOLUTION[0] / 4, RESOLUTION[1] / 4),
                      "blue": (3 * RESOLUTION[0] / 4, 3 * RESOLUTION[1] / 4)}


# bullet
BULLETS = {"normal": {"vel": 500 / FPS, "l_time": 500, "size": 6, "color": BLACK, "reload_time": 300, "dmg":20},
           "berta": {"vel": 1000 / FPS, "l_time": 1000, "size": 10, "color": BLUE, "reload_time": 1000, "dmg":40}}




