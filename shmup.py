 # Shmup game
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
INV_TIME = 5000


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PRPLE = (255, 0, 255)
# initialize pygame and create window
# pygame.joystick.init()
# pygame.joystick.get_count()
# pygame.joystick.Joystick
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
max_shield = 100.0

# fonts. arial, Sierf, Serif, Serif Bold, Sans serif, Monspace, Russo One, Exo 2,
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def newmetle():
    m = Metle()
    all_sprites.add(m)
    metles.add(m)


def draw_shield_bar(surf, x, y, shield):
    if shield < 0:
        shield = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (shield / max_shield) * BAR_LENGTH # (shield/max_shield) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (52, 60))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = max_shield
        self.shoot_delay = 190
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()



    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.power >= 3 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 10:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom =  HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
                self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()


    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = random.randrange(20,40)
        self.image_orig = pygame.transform.scale(random.choice(meteor_images),(self.radius*2, self.radius*2))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)
            self.speedy = random.randrange(5, 25)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (20, 50))
         # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10



    def update(self):
        self.rect.y += self.speedy
        # kill it if it move off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = pygame.transform.scale(powerup_images[self.type], (90, 90))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2




    def update(self):
        self.rect.y += self.speedy
        # kill it if it move off the top of the screen
        if self.rect.top >  HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
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
                self.rect = self.image.get_rect()
                self.rect.center = center






class Metle(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.radius = random.randrange(20,40)
            self.image_orig = pygame.transform.scale(random.choice(metle_img),(self.radius*2, self.radius*2))

            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 2)
            self.speedx = random.randrange(-2,2)
            self.rot = 0
            self.rot_speed = random.randrange(-8, 8)
            self.last_update = pygame.time.get_ticks()


        def rotate(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed) % 360
                self.image = pygame.transform.rotate(self.image_orig, self.rot)
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center

        def update(self):
            self.rotate()
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20 :
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-150, -50)
                self.speedy = random.randrange(5, 25)


def show_go_screen():
#    screen.blit(backgrownd, backgrownd_rect)
    draw_text(screen, "SHMUP!", 90, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin. p to pause. r to restart.", 19, WIDTH / 2, HEIGHT * 3 / 4)
    draw_text(screen, "L to shoot faster.", 19, WIDTH / 2, HEIGHT * 4 / 5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

backgrownd = pygame.image.load(path.join(img_dir, "Backgrownd15.png")).convert()
backgrownd_rect = backgrownd.get_rect()
player_img = pygame.image.load(path.join(img_dir,"8B.png"))
player_mini_img = pygame.transform.scale(player_img, (15, 17))
# player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "Bullet5.png"))
meteor_images = []
meteor_list = ["astroid1.png", "astroid2.png"]
metle_img = [pygame.image.load(path.join(img_dir,"metle.png"))]


for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for  i in range(4):
    filename = 'expl{}.png'.format(i+1)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'pow0.png'))
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'pow1.png'))

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew2.wav'))

expl_sounds = []
for snd in ['Expl3.wav', 'Expl4.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'blue_giant.ogg'))




pygame.mixer.music.play(loops=-1)
# Game loop

game_over = True
running = True
score = 0
while running:
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_p]:
        show_go_screen()

    if keystate[pygame.K_r]:
        show_go_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        metles = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerup = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        for i in range(2):
            newmetle()
        score = 0

    if score == 3500:
        y = random.randrange(-250, -150)
        speedy = random.randrange(20, 40)

    if score == 5500:
        y = random.randrange(-350, -250)
        speedy = random.randrange(60, 80)


    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        metles = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerup = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        for i in range(2):
            newmetle()
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    # check if the bullets hits a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    hits = pygame.sprite.groupcollide(metles, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > .9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerup.add(pow)
        newmob()
        newmetle()


    # check if the mod hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    hits = pygame.sprite.spritecollide(player, metles, False, pygame.sprite.collide_circle)

    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

        newmob()
        newmetle()
        if player.shield <= 0:
            player.hide()
            player.lives -= 1
            player.shield = 100.0

        if player.lives == 0:
            game_over = True

    hits = pygame.sprite.spritecollide(player, powerup, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100.0:
                player.shield = 100.0

        if hit.type == 'gun':
            player.powerup()




    # Draw / render
    screen.fill(BLACK)
    screen.blit(backgrownd, backgrownd_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score),18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    pygame.display.flip()
pygame.quit()
