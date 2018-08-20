from colors import *
#       tank
tank_speed = 5
turn_speed = 2
tank_gear = {0:0, 1:tank_speed, -1:-tank_speed}

#       bullet
bullets = {"normal":{"vel":50, "l_time":5, "size":6, "color":BLUE, "reload_time":0.5}
          }
#       display
FPS = 30
resolution = (1820, 1080)