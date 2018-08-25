# A TOP DOWN TANK BATTLE GAME
# playing music: Playonloop.com


from init import *
from mainloop import App

if __name__ == '__main__':
    surf = initialize_game()
    mainloop = App(surf)
    mainloop.show_start_screen()
    while mainloop.running:
        mainloop.start()
        mainloop.show_go_screen()
