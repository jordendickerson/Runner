import pygame as pg
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

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

        self.jumping = False
        self.sliding = False

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.acc.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.acc.x < 0:
                    self.pos.x = hits[0].rect.right
                self.acc.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.acc.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.acc.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.acc.y = 0
                self.rect.y = self.pos.y

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        # get key pressed
        keys = pg.key.get_pressed()
        # key functions
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC - 1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y += PLAYER_ACC * 2
        if keys[pg.K_DOWN] and keys[pg.K_SPACE]:
            self.jump()
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        # stop player from leaving the screen
        if self.pos.x > (WIDTH):
            self.pos.x = WIDTH
        if self.pos.x < -PLAYER_WIDTH:
            self.pos.x = -PLAYER_WIDTH
            self.pos.y = 60
        if self.pos.y < 20:
            self.pos.y = 20
            self.vel.y = 0.25
        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.acc.y += -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -2:
                self.vel.y = -2


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE