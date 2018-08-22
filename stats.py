from colors import *

#       display
FPS = 60  # calc speed as well
resolution = (1000, 1000)
fullscreen = False

#       tank
tank_speed = 150 / FPS
turn_speed = 60 / FPS
tank_gear = {0: 0,
             1: tank_speed,
             -1: -tank_speed}

#       bullet
bullets = {"normal": {"vel": 1500 / FPS, "l_time": 5, "size": 6, "color": BLACK, "reload_time": 0.5},
           "berta": {"vel": 3000 / FPS, "l_time": 10, "size": 50, "color": BLUE, "reload_time": 2}}
