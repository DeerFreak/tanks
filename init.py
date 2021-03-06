import pygame
from colors import *
from tank_class import *
from stats import *
from spritesheet import *
from sprites import *
from tiled_map import TiledMap
from random import choice

def initialize_game():
    pg.init()
    pg.mixer.init()
    if FULLSCREEN:
        surf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        surf = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(NAME)
    
    surf.fill(WHITE)
    pygame.display.update()

    return surf

def load_App_data(game):
    game.dir = path.dirname(__file__)
    game.img_dir = path.join(game.dir, "img")
    game.snd_dir = path.join(game.dir, "snd")
    game.map_dir = path.join(game.dir, "map")
    # graphics
    game.expl1 = Spritesheet(path.join(game.img_dir, EXPL1))
    game_icon = pg.image.load(path.join(game.img_dir, 'icon.png'))
    pg.display.set_icon(game_icon)

    game.graphics = Spritesheet(path.join(game.img_dir, "sheet_tanks.png"))
    # Tanks
    game.img_tanks = {}
    for color in ["red", "blue"]:
        img = pg.Surface((83 / 2, 100 / 2))  # 88
        body = game.graphics.get_image(*TANK_IMG_DIC[color][0])
        barrel = game.graphics.get_image(*TANK_IMG_DIC[color][1])
        barrel.set_colorkey(BLACK)
        img.blit(body, (0, 10))
        img.blit(barrel, (14, 0))
        img = pg.transform.rotate(img, -90)
        img.set_colorkey(BLACK)
        img.convert()
        game.img_tanks[color] = img

    # map
    game.map = TiledMap(path.join(game.map_dir, 'level1.tmx'))
    game.map_img = game.map.make_map()
    game.map_rect = game.map_img.get_rect()
    
    # bullets
    game.img_bullets = {}
    for bullet in BULLETS:
        game.img_bullets[bullet] = {}
        for color in ["red", "blue"]:
            img = game.graphics.get_image(*BULLET_IMG_DIC[bullet][color])
            img = pg.transform.rotate(img, -90)
            img.set_colorkey(BLACK)
            img.convert()
            game.img_bullets[bullet][color] = img
    # explosions
    game.img_explosions = {}
    game.img_explosions["normal"] = {}
    for type in EXPLOSION_IMG_DICT:
        game.img_explosions["normal"][type] = []
        for frame in EXPLOSION_IMG_DICT[type]:
            img = game.graphics.get_image(*frame)
            img.set_colorkey(BLACK)
            img.convert()
            game.img_explosions["normal"][type].append(img)
    # background
    img = (game.graphics.get_image(*BG_IMG_DICT[BG_ATM]),game.graphics.get_image(*BG_IMG_DICT["dirt"]))
    game.img_ground = pg.Surface((WIDTH, HEIGHT))
    for coloum in range(0, WIDTH, TILESIZE):
        for row in range(0, HEIGHT, TILESIZE):
            game.img_ground.blit(choice(img), (coloum, row))
    game.img_ground_rect = game.img_ground.get_rect()

    # sound
    game.shot_snd_dir = {}
    game.shot_snd_dir["normal"] = pg.mixer.Sound(path.join(game.snd_dir, "shot0.wav"))
    game.shot_snd_dir["berta"] = pg.mixer.Sound(path.join(game.snd_dir, "shot1.wav"))
    game.expl_snd_dir = {}
    game.expl_snd_dir["normal"] = pg.mixer.Sound(path.join(game.snd_dir, "expl0.wav"))