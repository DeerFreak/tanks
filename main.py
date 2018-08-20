from init import *
from mainloop import App
from stats import resolution, FPS, fullscreen
if __name__ == '__main__':
    game = initialize_game(resolution, fullscreen)
    mainloop = App(game, FPS)
    mainloop.start()