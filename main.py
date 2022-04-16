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
        self.SPAWN_PLAT = pg.USEREVENT+1
        pg.time.set_timer(self.SPAWN_PLAT, 1000)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.player = Player(self)
        g = Ground(self, 0, HEIGHT - 40, 1200, 40)
        # for plat in PLATFORM_LIST:
        #     Platform(self, *plat)
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
            # if player slides while on platform, add velocity
            if hits and self.player.sliding:
                self.player.vel.y = -PLAYER_ACC * 2.1
                self.player.vel.x += 0.25
            #move player with platform if standing on one
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits and not self.player.sliding:
                self.player.pos.x -= PLATFORM_SPEED
            #move player back if hitting pipe
            hits = pg.sprite.spritecollide(self.player, self.pipes, False)
            if hits:
                self.player.vel.x -= PLATFORM_SPEED

        #move and kill platforms
        for plat in self.platforms:
            plat.rect.x -= PLATFORM_SPEED
            if plat.rect.x < -600:
                plat.kill()
        #move and kill pipes
        for pipe in self.pipes:
            pipe.rect.x -= PLATFORM_SPEED
            if pipe.rect.x < -600:
                pipe.kill()

        #if player goes off left side of screen, end game
        if self.player.pos.x < 0:
            self.running = False


    def events(self):
        for event in pg.event.get():
            #ON QUIT
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #ON KEYDOWN
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.sliding = True
            #ON KEYUP
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE or event.key == pg.K_w or event.key == pg.K_UP:
                    # self.player.jump_cut()
                    pass
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.sliding = False
            #EVERY SECOND SPAWN PLAT
            if event.type == self.SPAWN_PLAT:
                self.platx = random.randrange(WIDTH + 300, WIDTH + 500)
                self.platy = random.randrange(50, 400)
                pct = random.randrange(100)
                if pct > 25:
                    Platform(self, self.platx, self.platy, 200, 20)
                else:
                    pipe_pct = random.randrange(1, 4)
                    if pipe_pct == 1:
                        for pipe in PIPE_1:
                            Pipe(self, *pipe)
                    if pipe_pct == 2:
                        for pipe in PIPE_2:
                            Pipe(self, *pipe)
                    if pipe_pct == 3:
                        for pipe in PIPE_3:
                            Pipe(self, *pipe)
                    print(pipe_pct)

    def draw(self):
        #Draw sprites
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        #after drawing, flip display
        pg.display.flip()

    def draw_pipe(self):
        x = WIDTH + 2250
        y = -200
        w = 20
        h = 400
        Platform(self, x, y, w, h)
        Platform(self, x, -y + h, w, h)

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