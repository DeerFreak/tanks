# shmup game
# music by Music by Matthew Pablo / www.matthewpablo.com

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

WIDTH   = 480
HEIGHT  = 600
FPS     = 60

POWERUP_TIME = 5000

# define colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
GOLD  = (255, 185, 15)

# initialize pygame and create window
pygame.init()
pygame.mixer.init() # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial") # finds closest match to "arial" on computer
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf ,x , y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    draw_text(screen, "Shoot em up!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)    
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38)) # loads scaled picture
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        
        self.hidden = False # picture flag
        self.hidden_timer = pygame.time.get_ticks()
       
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        if self.power > 1 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                random.choice(shoot_sounds).play()
            
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                random.choice(shoot_sounds).play()
    
    def hide(self):
        # hises player temorarily
        self.hidden = True
        self.hidden_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH, HEIGHT + 700)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width) # so it does not stick out
        self.rect.bottom = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.right < -10 or self.rect.left > WIDTH + 10: # rerandomise at top
            self.rect.x = random.randrange(WIDTH - self.rect.width) 
            self.rect.bottom = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (9, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center

# load all game graphics
background = pygame.image.load(path.join(img_dir, "bg5.jpg")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

meteor_images = []
meteor_list = [ "meteorBrown_big1.png","meteorBrown_big2.png","meteorBrown_big3.png","meteorBrown_big4.png",\
                "meteorBrown_med1.png","meteorBrown_med3.png",\
                "meteorBrown_small1.png","meteorBrown_small2.png","meteorBrown_tiny1.png","meteorBrown_tiny2.png",\
                "meteorGrey_big1.png","meteorGrey_big2.png","meteorGrey_big3.png","meteorGrey_big4.png",\
                "meteorGrey_med1.png","meteorGrey_med2.png",\
                "meteorGrey_small1.png","meteorGrey_small2.png","meteorGrey_tiny1.png","meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
for i in range(11):
    filename = f"explosion{i}.png"
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim["sm"].append(img_sm)

# load all game sounds
shoot_sounds = []
shoot_list = ["Laser_Shoot.wav", "Laser_Shoot1.wav"]
for shot in shoot_list:
    shoot_sounds.append(pygame.mixer.Sound(path.join(snd_dir, shot)))
explosion_sounds = []
explosion_list = ["Explosion1.wav", "Explosion2.wav"]
for sound in explosion_list:
    explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, sound)))
pygame.mixer.music.load(path.join(snd_dir, "music.mp3"))
pygame.mixer.music.set_volume(0.4)
power_sound = pygame.mixer.Sound(path.join(snd_dir, "pow_sound.wav"))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, "shield_sound.wav"))

powerup_images = {}
powerup_images["shield"] = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
powerup_images["gun"] = pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()

pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        # setup game
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(16):
            new_mob()

        score = 0

    # keep running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # True would delete colliding obj
    for hit in hits:
        player.shield -= hit.radius * 2
        new_mob()
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        if player.shield <= 0:
            death_expl = Explosion(player.rect.center, "lg")
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            player.shield = 100
            random.choice(explosion_sounds).play()
            
    # if the player died and the explosion has finished -> end game
    if player.lives == 0 and not death_expl.alive():
        game_over = True

    # check to see if bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # both obj get deletet if hit
    for hit in hits:
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        new_mob()
        random.choice(explosion_sounds).play()
    
    #check to see if powerup hit player
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
                shield_sound.play()

        if hit.type == "gun":
            player.powerup()
            power_sound.play()

    score += 0.2
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect) # copie the pixels of one thing onto anoter
    all_sprites.draw(screen)
    draw_text(screen, str(int(score)), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()