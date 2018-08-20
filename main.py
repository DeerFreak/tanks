from init import *
from mainloop import App
from stats import resolution, FPS
if __name__ == '__main__':
    resolution = (1000,1000)
    game = initialize_game(resolution)
    mainloop = App(game, FPS)
    mainloop.start()