from init import *
from mainloop import App

if __name__ == '__main__':
    resolution = (1000,1000)
    game = initialize_game(resolution)
    mainloop = App(game)
    mainloop.start()