from init import *
from mainloop import App
from stats import FPS, fullscreen
if __name__ == '__main__':
    surf = initialize_game(fullscreen)
    mainloop = App(surf, FPS)
    mainloop.start()
