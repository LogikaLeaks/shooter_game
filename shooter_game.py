from pygame import *
from random import randint
from math import *


# ****************************** CLASESS ******************************



class GameSprite(sprite.Sprite):
    def __init__(self, filename_img, x, y, width, height, speed):
        
        sprite.Sprite.__init__(self)
        self.image = image.load(filename_img)
        self.image = transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        if key.get_pressed()[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        elif key.get_pressed()[K_RIGHT] and self.rect.x <= SIZE[0] - self.rect.width - 10:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 500:
            self.rect.y -= self.speed
        else:
            self.__del__()


class Enemy(GameSprite):
    def update(self):
        if self.rect.y <= SIZE[1]:
            self.rect.y += self.speed
        else:
            self.rect.y = randint(-200, -50)
            self.rect.x = randint(0, SIZE[0] - self.rect.width)
            global missed
            missed += 1

class Asteroid(GameSprite):
    def __init__(self, filename_img, x, y, width, height, speed, angle):
        super().__init__(filename_img, x, y, width, height, speed)
        self.angle = angle
        
    def update(self):
        if self.rect.y <= SIZE[1] and self.rect.x <= SIZE[0]:
            self.rect.y += self.speed
            self.rect.x += cos(self.angle)/sin(self.angle)
        else:
            self.rect.y = randint(-200, -50)
            self.rect.x = randint(0, SIZE[0] - self.rect.width)




# ****************************** VARIABLES ******************************



# WND SIZE
SIZE = (700, 500)

# -
missed = 0
score = 0

# THE STATUS OF GAME LOOP(GL)  
GLstatus = True

# clock
clock = time.Clock()

# PLAYER WITH 5 ENEMIES
player  = Player("rocket.png", 5, 400, 50, 80, 9)

enemies = sprite.Group()
for i in range(0, 5):
    enemy = Enemy("ufo.png", randint(0, SIZE[0]), randint(-100, -50), 50, 50, randint(1, 2))

    enemies.add(enemy)

bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(0, 5):
    asteroid = Asteroid("asteroid.png", randint(0, SIZE[0]), randint(0, 10), 50, 50, randint(1, 2), randint(0, 90))

    asteroids.add(asteroid)


# FONT
font.init()



# ****************************** INITIALATION ******************************



# CREATING EMPTY WINDOW WITH CAPTION "!!!!!"
# AND SETTING MUSIC
# CREATING THE SCORE COUNTER AND DISPLAYING IT AT THE WND

init()
window = display.set_mode(SIZE)
display.set_caption("!!!!!")
background = transform.scale(image.load("galaxy.jpg"), SIZE)


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(0, 0)



# ****************************** GAME LOOP ******************************



while GLstatus:
    window.blit(background, (0, 0))


    scoreFONT = font.SysFont("Arial", 32).render("Score: " + str(score), True, (255, 255, 255))
    missedFONT = font.SysFont("Arial", 32).render("Missed: " + str(missed), True, (255, 255, 255))
    window.blit(scoreFONT, (10, 10))
    window.blit(missedFONT, (10, 32 + 10))

    player.reset()

    asteroids.draw(window)
    enemies.draw(window)
    bullets.draw(window)

    if missed >= 3:
        lost = font.SysFont("Arial", 32).render("You lost, because you had missed 3 or more aliens", True, (255, 255, 255))
        window.blit(lost, (100, 318))
        
        for ev in event.get(): 
            if ev.type == QUIT:
                GLstatus = False
            if ev.type == KEYDOWN:
                if ev.key == K_r:
                    GLstatus = True
                    missed = 0
                    score = 0
                    bullets = sprite.Group()

                    for enemy in enemies:
                        enemy.rect.x = randint(0, SIZE[0])
                        enemy.rect.y = randint(-100, -50)

        display.update()
        continue

    elif sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
        lost = font.SysFont("Arial", 32).render("You lost because you had crashed into the alien.", True, (255, 255, 255))
        window.blit(lost, (100, 318))
        
        for ev in event.get():
            if ev.type == QUIT:
                GLstatus = False
            if ev.type == KEYDOWN:
                    if ev.key == K_r:
                        GLstatus = True
                        missed = 0
                        score = 0
                        bullets = sprite.Group()

                        for enemy in enemies:
                            enemy.rect.x = randint(0, SIZE[0])
                            enemy.rect.y = randint(-100, -50)

        display.update()
        continue
    elif score >= 10:
        winning = font.SysFont("Arial", 32).render("You won!!! Congrultations!!", True, (255, 255, 255))
        window.blit(winning, (100, 318))

        for ev in event.get():
            if ev.type == QUIT:
                GLstatus = False

            if ev.type == KEYDOWN:
                if ev.key == K_r:
                    GLstatus = True
                    missed = 0
                    score = 0
                    bullets = sprite.Group()

                    for enemy in enemies:
                        enemy.rect.x = randint(0, SIZE[0])
                        enemy.rect.y = randint(-100, -50)

        display.update()
        continue



    for ev in event.get():
        if ev.type == QUIT:
            GLstatus = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE: 
                mixer.Sound("fire.ogg").play() 
    
                bullets.add(Bullet("bullet.png", player.rect.x + player.rect.width/2 - 5, player.rect.y, 10, 10, 10))

    
            
    for enemy in sprite.groupcollide(enemies, bullets, False, True):
                
            score += 1
            enemy.rect.x = randint(0, SIZE[0])
            enemy.rect.y = randint(-100, -50)

    for asteroid in sprite.groupcollide(asteroids, bullets, False, True):
                
            asteroid.rect.x = randint(0, SIZE[0])
            asteroid.rect.y = randint(-100, -50)
            asteroid.angle = randint(0, 90)

    for bullet in bullets:
        if bullet.rect.y >= SIZE[1]:
            bullets.remove(bullet)


    bullets.update()
    enemies.update()
    asteroids.update()

    player.update()


    display.update()
    clock.tick(120)