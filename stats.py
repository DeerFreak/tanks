# Colors
WHITE   = (255, 255,255)
BLUE    = (0,   0,  255)
RED     = (255, 0,  0)
BLACK   = (0,   0,  0)

#       display
FPS = 60  # calc speed as well
resolution = (1000, 800)
fullscreen = False
TANK_LAYER = 3
BULLET_LAYER = 2
WALL_LAYER = 4
BG_LAYER = 0
POW_LAYER = 1


#       tank
tank_speed = 200 / FPS
turn_speed = 120 / FPS
tank_gear = {0: 0,
             1: tank_speed,
             -1: -tank_speed}
TANK_START_POS = {"red": (resolution[0] / 4, resolution[1] / 4),
                      "blue": (3 * resolution[0] / 4, 3 * resolution[1] / 4)}


#       bullet
BULLETS = {"normal": {"vel": 500 / FPS, "l_time": 5, "size": 6, "color": BLACK, "reload_time": 0.2, "dmg":20},
           "berta": {"vel": 1000 / FPS, "l_time": 10, "size": 10, "color": BLUE, "reload_time": 1, "dmg":40}}



