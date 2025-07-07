import time
import pygame as pg
from random import randint

pg.init()

 
GREEN = (0, 255, 0)
win_size = (800, 600)
x, y = 0, 1
platon = []
platonchik = pg.sprite.Group()
bullets = pg.sprite.Group()
meteors = pg.sprite.Group()
 
# https://pastebin.com/raw/xsDrxLaH
class BaseSprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed_x=0, speed_y=0):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.image = pg.transform.scale(pg.image.load(filename), (w, h))
        self.speed_x = speed_x
        self.speed_y = speed_y
 
    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
 
 
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
 
 
class Hero(BaseSprite):
    energy = 0
    max_energy = 25
    points = 0
 
    def update(self):
        self.energy += 1
        keys = pg.key.get_pressed()
 
        if keys[pg.K_a]:
            self.rect.x -= self.speed_x
            if self.rect.x < 0:
                self.rect.x = 0
        if keys[pg.K_d]:
            self.rect.x += self.speed_x
            if self.rect.x > win_size[x] - self.rect.width:
                self.rect.x = win_size[x] - self.rect.width
        if keys[pg.K_s]:
            self.rect.y += self.speed_y
            if self.rect.x > win_size[x] - self.rect.height:
                self.rect.x = win_size[x] - self.rect.height
        if keys[pg.K_w]:
            self.rect.y -= self.speed_y
            if self.rect.y < 0:
                 self.rect.x = 0 
        if keys[pg.K_SPACE]:
            self.fire()
 
    def fire(self): 
        if self.energy >= self.max_energy:
            self.energy = 0
            fire_snd.play()
            bullet  = Bullet('bhrfs.png',
                        self.rect.x, self.rect.y,
                        15, 40, 0, -4)
            bullets.add(bullet)
 
 
 
class Star(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y > win_size[y]:
            platon.remove(self)
class Meteor(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y > win_size[y]:
            meteors.remove(self)
 
class Bullet(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y < 0:
            bullets.remove(self)
 
 
class UFO(BaseSprite):
    def update(self):
        global ufo_missed
        super().update()
        if self.rect.y > win_size[y]:
            platonchik.remove(self)
            ufo_missed += 1
 
 
 
def make_star():
    speed = randint(1, 10)
    size = speed * 5
    star = Star('staRR.png', randint(0, win_size[x]),
                    -50, size, size, 0, speed)
    platon.append(star)
 
 
def make_meteor():
    speed_y = randint(1, 10)
    speed_x = randint(-3, 3)
    size = randint(4, 10) * 10
    xx = randint(-100, win_size[x] + 100)
    yy = -200
    meteor = Meteor('asteroid.png', xx, yy, size, size, speed_x, speed_y)          
    meteors.add(meteor)
 
def make_ufo():
    speed = randint(2, 4)
    size = 80
    ufo = UFO('ufo.png', randint(0, win_size[x]),
                    -100, 80, 60, 0, speed)
    platonchik.add(ufo)
 
 
 
def set_text(text, x, y, color=(255,255,200)):
    mw.blit(
        font1.render(text, True, color), (x, y)
    )
 
font1 = pg.font.Font(None, 36)
 
# mw = pg.display.set_mode(win_size, pg.FULLSCREEN)
mw = pg.display.set_mode(win_size)
clock = pg.time.Clock()
 
ufo_missed = 0
 
fon = pg.image.load("spacd.jpg")
fon = pg.transform.scale(fon, win_size)
 
# fon_win = pg.image.load("win.jpg")
# fon_win = pg.transform.scale(fon_win, (800, 600))
 
# fon_go = pg.image.load("gameover.jpg")
# fon_go = pg.transform.scale(fon_go, (800, 600))
 
 
 
 
hero = Hero('taksa.png', 1, 500, 80, 80, 5, 5)
 
 
 
star = Star('staRR.png', 400, -50, 10, 10, 0, 3)
 
pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
fire_snd = pg.mixer.Sound('fire.ogg')
# pg.mixer.music.load('jungles.ogg')
# pg.mixer.music.play()
# kick = pg.mixer.Sound('kick.ogg')
# gold_sound = pg.mixer.Sound('money.ogg')
 
play = True
game = True
 
ticks = 0
 
 
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
 
    if play:
        if ticks % 15 == 0:
            make_star()
 
        if ticks % 60 == 0:
            make_ufo()
        if ticks % 60 == 0:
            make_meteor()
 
        mw.blit(fon, (0,0))
 
        hero.update()
        hero.draw()
 
        for star in platon:
            star.update()
            star.draw()
 
        for ufo in platonchik:
            ufo.update()
            ufo.draw()
 
        for bullet in bullets:
            bullet.update()
            bullet.draw()
 
        meteors.update()
        meteors.draw(mw)
 
        collides =  pg.sprite.groupcollide(bullets, platonchik, True, True)
        for bullet, ufo in collides.items():
                hero.points += 1
 
 
        set_text(f'Пропущено: {ufo_missed}', 10, 60)
        set_text(f'Очки: {hero.points}', 10, 25)
 
 
 
    pg.display.update()
    clock.tick(60)
    ticks += 1
 