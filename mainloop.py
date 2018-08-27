import pygame as pg
import time as t
from pygame.locals import *
import numpy as np
from stats import *
from tank_class import Tank
from os import path
from spritesheet import Spritesheet
from sprites import *
from wall_class import *
import random

class App(object):
    def __init__(self, surf):
        self.surf = surf
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.clock = pg.time.Clock()
        self.event_dict = {"w": False, "a": False, "s": False, "d": False, " ": False,\
                           "đ": False, "ē": False, "Ē": False, "Ĕ": False, "p": False,\
                           "c": False, "o": False}
        self.keys = pg.key.get_pressed()
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")
        self.snd_dir = path.join(self.dir, "snd")
        # graphics
        self.expl1 = Spritesheet(path.join(self.img_dir, EXPL1))
        game_icon = pg.image.load(path.join(self.img_dir, 'icon.png'))
        pg.display.set_icon(game_icon)

        self.graphics = Spritesheet(path.join(self.img_dir, "sheet_tanks.png"))
        # Tanks
        self.img_tanks = {}
        # map
        self.map = Map(path.join(self.dir, "map0.txt"))

        for color in ["red", "blue"]:
            img = pg.Surface((83 / 2, 100 / 2)) # 88
            body = self.graphics.get_image(*TANK_IMG_DIC[color][0])
            barrel = self.graphics.get_image(*TANK_IMG_DIC[color][1])
            barrel.set_colorkey(BLACK)
            img.blit(body, (0, 10))
            img.blit(barrel, (14,0))
            img = pg.transform.rotate(img, -90)
            img.set_colorkey(BLACK)
            img.convert()
            self.img_tanks[color] = img
        # bullets
        self.img_bullets = {}
        for bullet in BULLETS:
            self.img_bullets[bullet] = {}
            for color in ["red", "blue"]:
                img = self.graphics.get_image(*BULLET_IMG_DIC[bullet][color])
                img = pg.transform.rotate(img, -90)
                img.set_colorkey(BLACK)
                img.convert()
                self.img_bullets[bullet][color] = img
        # explosions
        self.img_explosions = {}
        self.img_explosions["normal"] = {}
        for type in EXPLOSION_IMG_DICT:
            self.img_explosions["normal"][type] = []
            for frame in EXPLOSION_IMG_DICT[type]:
                img = self.graphics.get_image(*frame)
                img.set_colorkey(BLACK)
                img.convert()
                self.img_explosions["normal"][type].append(img)
        # background
        img = self.graphics.get_image(*BG_IMG_DICT[BG_ATM])
        self.img_ground = pg.Surface((WIDTH, HEIGHT))
        for coloum in range((2 * WIDTH // 128) + 1):
            for row in range((2 * HEIGHT // 128) + 1):
                self.img_ground.blit(img, (coloum * 128 / 2, row * 128 / 2))
        self.img_ground_rect = self.img_ground.get_rect()


        # sound
        self.shot_snd_dir = {}
        self.shot_snd_dir["normal"] = pg.mixer.Sound(path.join(self.snd_dir, "shot0.wav"))
        self.shot_snd_dir["berta"] = pg.mixer.Sound(path.join(self.snd_dir, "shot1.wav"))
        self.expl_snd_dir = {}
        self.expl_snd_dir["normal"] = pg.mixer.Sound(path.join(self.snd_dir, "expl0.wav"))

    def start(self):
        self.all_sprites = pg.sprite.Group()
        self.tanks = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "a":
                    self.tank1 = Tank(self, "red", col, row)
                if tile == "b":
                    self.tank2 = Tank(self, "blue", col, row)

        self.tank2_group = pg.sprite.Group()
        self.tank2_group.add(self.tank2)
        # spawing random walls
        while len(self.walls) < WALLS_NUMBER:
            (x, y) = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            ang = random.randint(0, 360)
            wall = Wall(self, (x, y), ang)
            if pg.sprite.spritecollide(wall, self.walls, False, pg.sprite.collide_mask) or \
                pg.sprite.spritecollide(wall, self.tanks, False, pg.sprite.collide_mask):
                wall.kill()
            self.walls.add(wall)

        self.event_keys = {"c": self.tank1.next_weapon,
                           "o": self.tank2.next_weapon,
                           "č": pg.quit}  # Quit on "-" num block
        pg.mixer.music.load(path.join(self.snd_dir, "battle_march.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(MUSIC_VOL_INGAME)


        while self.tank1.health > 0 and self.tank2.health > 0:
            self.clock.tick(FPS)
            self.events()
            self.all_sprites.update()
            # collision of tanks
            (self.tank1.sign, self.tank2.sign) = (-1,) * 2 # for all tank collisions
            if pg.sprite.spritecollide(self.tank1, self.tank2_group, False): # to improve performance
                if pg.sprite.spritecollide(self.tank1, self.tank2_group, False, pg.sprite.collide_mask):
                    self.tanks.update()
            # collision of tanks & walls
            """
            if pg.sprite.groupcollide(self.tanks, self.walls, False, False, pg.sprite.collide_mask): # to improve performance
                collisions = pg.sprite.groupcollide(self.tanks, self.walls, False, False, pg.sprite.collide_mask)
                for col in collisions:
                    col.update()
            """
            (self.tank1.sign, self.tank2.sign) = (1,) * 2 # reset sign after tank collisions

            pg.sprite.groupcollide(self.bullets, self.walls, True, False)
            self.bullets.update()
            self.check_bullet_hit()
            self.plot()

         # when signle game is finished
        while len(self.explosions) > 0:
            self.clock.tick(FPS)
            self.explosions.update()
            self.plot()
        pg.mixer.music.fadeout(500)


    def events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.running = False
                pg.quit()
            if event.type == KEYDOWN:
                try:
                    self.event_keys[chr(event.key)]()
                except:
                    pass

            self.keys = pg.key.get_pressed()

    def check_bullet_hit(self):
        hits = pg.sprite.groupcollide(self.tanks, self.bullets, False, False)
        for hit in hits:
            if hit != hits[hit][0].shooter:
                hit.health -= hits[hit][0].dmg
                Explosion(self, hits[hit][0].rect.center, self.img_explosions["normal"]["white"])
                hits[hit][0].kill()

    def plot(self):
        self.surf.fill(BG_COLOR)
        self.surf.blit(self.img_ground, self.img_ground_rect)
        self.draw_text(f"Player 1: {str(self.tank1.health)}HP", 30, RED, 120, 5)
        self.draw_text(f"Player 2: {str(self.tank2.health)}HP", 30, BLUE, 120, 35)
        # Game Loop - draw
        self.all_sprites.draw(self.surf)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x, y)
        self.surf.blit(text_surf, text_rect)

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "ls_music.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(MUSIC_VOL_LS)
        self.surf.fill(BG_COLOR)
        self.draw_text(NAME, 50, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("controls1: wasd c v", 22, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("controls2: Arrows o p", 22, BLUE, WIDTH / 2, HEIGHT / 2 + 25)
        self.draw_text("Press any key to play", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "ls_music.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(1.2)
        self.surf.fill(BG_COLOR)
        if self.tank1.health > 0:
            win_text = "Player 1 won!"
        else:
            win_text = "Player 2 won!"
        self.draw_text(f"{win_text}", 22, BLUE, WIDTH / 2, 10)
        self.draw_text("", 50, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f"", 22, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        if not self.running:
            return
        for sprite in self.all_sprites: # if one of them dies to clear space for new game
            sprite.kill()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False