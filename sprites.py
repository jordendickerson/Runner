import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self, self.game.all_sprites)
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        #get key pressed
        keys = pg.key.get_pressed()
        #key functions
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
        if keys[pg.K_DOWN]:
            self.acc.y += PLAYER_ACC
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
        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.acc.y += -PLAYER_JUMP


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w,h))
        self.image.fill(darkBlue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = game.all_sprites, game.ground
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w,h))
        self.image.fill(darkBlue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y