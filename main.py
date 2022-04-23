from settings import *
import sys
from sprites import *
from tilemap import *
import pygame as pg
from os import path
import random

#YOU MUST INSTALL PYGAME ON YOUR COMPUTER FOR THIS GAME TO RUN

#YOU MUST INSTALL PYGAME ON YOUR COMPUTER FOR THIS GAME TO RUN

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def load_data(self):
        self.map = Map(path.join(maps_Folder, 'card1.txt'))

    def quit(self):
        pg.quit()
        sys.exit()

    def new(self):
        #sprite groups
        self.all_sprites = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.deadly_platforms = pg.sprite.Group()
        #call load data
        self.load_data()
        #create map
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, (self.ground, self.all_platforms), GREEN)
                if tile == '2':
                    Wall(self, col, row, (self.deadly_platforms, self.all_platforms), RED)
                if tile == "P":
                    self.player = Player(self, col, row)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        #move the map
        for plat in self.all_platforms:
            plat.rect.x -= PLATFORM_SPEED
            #delete tile when it moves off screen. there is no going back
            if plat.rect.x < -100:
                plat.kill()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            # player stands on top of platform
            hits = pg.sprite.spritecollide(self.player, self.ground, False)
            if hits:
                self.player.jumping = False
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        #check for collisions between player and deadly objects / platforms
        hits = pg.sprite.spritecollide(self.player, self.deadly_platforms, False)
        if hits:
            self.playing = False
        #Update loops
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #Draw sprites
        self.screen.fill(GRAY)
        self.all_sprites.draw(self.screen)
        # Draw grid
        self.draw_grid()
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