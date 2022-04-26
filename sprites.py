import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import uniform
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        pg.sprite.Sprite.__init__(self, self.game.all_sprites)
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x * TILESIZE, y * TILESIZE)
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.last_shot = 0

        self.jumping = False
        self.sliding = False

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0 and hits[0].rect.top > self.rect.centery and hits[0].rect.bottom < self.rect.centery:
                    self.pos.x = hits[0].rect.left
                if self.vel.x < 0 and hits[0].rect.top > self.rect.centery and hits[0].rect.bottom < self.rect.centery:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def get_keys(self):
        # get key pressed
        keys = pg.key.get_pressed()
        # key functions
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC - 1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y += PLAYER_ACC * 2
            self.acc.x += PLAYER_ACC * 1.2
        if keys[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > FIRE_RATE:
            self.last_shot = now
            Bullet(self.game, self.pos, (self.game.all_sprites, self.game.bullets))

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        #get key input
        self.get_keys()
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # stop player from leaving the screen
        if self.pos.x > (WIDTH):
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 20:
            self.pos.y = 20
            self.vel.y = 0.25
        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.acc.y += -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -2:
                self.vel.y = -2


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, group, color):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Trigger(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, group, speed_y = 0):
        super(Bullet, self).__init__()

        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Bullet image

        self.image = pg.Surface((10,10))
        self.image.fill(BLACK)
        # self.image = pg.transform.scale(self.image, (10, 20))
        # self.image.set_colorkey(BLACK)


        # Bullet rect & radius
        self.rect = self.image.get_rect()
        self.rect.centerx = pos.x + BARREL_OFFSET
        self.rect.centery = pos.y - BARREL_OFFSET
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)


        # Bullet speed
        self.moveSpeed = BULLET_SPEED
        self.speed_x = -self.moveSpeed
        self.speed_y = speed_y

    def update(self):
        self.rect.centery += self.speed_y
        self.rect.centerx -= self.speed_x
        if self.rect.bottom < -15:
            self.kill()


