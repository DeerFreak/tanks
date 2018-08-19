from init import *
from mainloop import mainloop

if __name__ == '__main__':
    resolution = (1920,1080)
    game = initialize_game(resolution)
    mainloop(game)