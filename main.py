from settings import *
from sprites import *
import pygame as pg
import random

#YOU MUST INSTALL PYGAME ON YOUR COMPUTER FOR THIS GAME TO RUN

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.spawning = False
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.player = Player(self)
        g = Ground(self, 0, HEIGHT - 40, 1100, 40)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #Update loops
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            #player stands on top of platform
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.jumping = False
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            #move player with platform if standin on one
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits and not self.player.sliding:
                self.player.pos.x -= PLATFORM_SPEED
        #move and kill platforms
        for plat in self.platforms:
            plat.rect.x -= PLATFORM_SPEED
            if plat.rect.x < -600:
                plat.kill()

        # spawn new platforms to keep same average number
        while len(self.platforms) < 8:
            self.platx = random.randrange(WIDTH + 500, WIDTH + 1500)
            self.lastx = 5000
            self.platy =  random.randrange(50, 400)
            self.lasty = 5000

            while (self.lastx - self.platx) < 250 and (self.lasty - self.platy) < 250:
                self.platx = random.randrange(WIDTH + 500, WIDTH + 1500)
                self.platy = random.randrange(50, 400)
            self.lastx = self.platx
            self.lasty = self.platy
            print(self.lasty)
            Platform(self, self.platx, self.platy, 200, 20)


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.sliding = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE or event.key == pg.K_w or event.key == pg.K_UP:
                    # self.player.jump_cut()
                    pass
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.sliding = False

    def draw(self):
        #Draw sprites
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        #after drawing, flip display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()