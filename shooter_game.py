#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as tm

#создай окно 
window = display.set_mode((700, 450))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 450))

game = True
clock = time.Clock()
FPS = 60
points = 0
miss = 0
ammo = 0
fire_count = 0
rel_time = False

mixer.init()
font.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_ = mixer.Sound('fire.ogg')
font1 = font.SysFont('Arial', 70)
font2 = font.SysFont('Arial', 30)
win = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed

        if keys_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed  
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 10, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__(player_image, player_x, player_y, player_speed, w, h)
    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            miss += 1

class Meteor(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__(player_image, player_x, player_y, player_speed, w, h)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__(player_image, player_x, player_y, player_speed, w, h)
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 45, 370, 10, 45, 75)

finish = False

bullets = sprite.Group()

meteors = sprite.Group()
for i in range(3):
    meteor = Meteor('asteroid.png', randint(0, 600), 0, randint(1, 3), 60, 40)
    meteors.add(meteor)

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 600), 0, randint(1, 3), 60, 40)
    monsters.add(enemy)

#создай 2 спрайта и размести их на сцене

#обработай событие «клик по кнопке "Закрыть окно"»
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fire_count <= 5 and rel_time == False:
                    player.fire()
                    fire_.play()
                    fire_count += 1

                if fire_count > 5 and rel_time == False:
                    rel_time = True
                    start = tm()


    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        monsters.draw(window)
        meteors.draw(window)
        bullets.draw(window)
        player.update()
        monsters.update()
        meteors.update()
        bullets.update()
        points_counter = font2.render('Счет: '+str(points), True, (255, 255, 255))
        miss_counter = font2.render('Пропущено: '+str(miss), True, (255, 255, 255))
        window.blit(points_counter, (0, 0))
        window.blit(miss_counter, (0, 20))

        monsters_list = sprite.groupcollide(monsters, bullets, True, True)
    
        for monster in monsters_list:
            points += 1
            enemy = Enemy('ufo.png', randint(0, 600), 0, randint(1, 3), 60, 40)
            monsters.add(enemy)

        if sprite.spritecollide(player, monsters, False) or miss >= 3 or sprite.spritecollide(player, meteors, False):
            lose = font1.render('YOU LOSE!', True, (255, 0, 0))
            window.blit(lose, (200, 200))
            finish = True

        if points >= 10:
            win = font1.render('YOU WON!', True, (255, 215, 0))
            window.blit(win, (200, 200))
            finish = True

        if rel_time == True:
            curr_time = tm()
            if curr_time - start <= 1:
                reload_text = font2.render('wait, reloading!', True, (155, 0, 0))
                window.blit(reload_text, (250, 430))
            else:
                fire_count = 0
                rel_time = False

    display.update()
    clock.tick(FPS)