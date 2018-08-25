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
FRAME_TICK_RATES = {"normal":2}

# music
MUSIC_VOL_INGAME = 0.2
MUSIC_VOL_LS = 1.2

#       tank
TANK_SPEED = 200 / FPS
TURN_SPEED = 120 / FPS
TANK_GEAR = {0: 0,
             1: TANK_SPEED,
             -1: -TANK_SPEED}
TANK_START_POS = {"red": (RESOLUTION[0] / 4, RESOLUTION[1] / 4),
                      "blue": (3 * RESOLUTION[0] / 4, 3 * RESOLUTION[1] / 4)}


#       bullet
BULLETS = {"normal": {"vel": 500 / FPS, "l_time": 5, "size": 6, "color": BLACK, "reload_time": 300, "dmg":20},
           "berta": {"vel": 1000 / FPS, "l_time": 10, "size": 10, "color": BLUE, "reload_time": 1000, "dmg":40}}

#       walls for testing
WALLS = [[(WIDTH / 2 , HEIGHT / 2), 70], [(WIDTH * 3 / 4 , HEIGHT  / 2), -30]]


