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
        self.paused = False
        self.title_font = path.join(assets_Folder, 'Pixeboy.ttf')
        self.plat_speed = PLATFORM_SPEED

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        #load map
        self.map = Map(path.join(maps_Folder, 'ground.txt'))
        #fonts
        self.title_font = path.join(assets_Folder, 'Pixeboy.ttf')
        #create screen dimmer
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

    def create_map(self, map):
        for row, tiles in enumerate(map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, (self.ground, self.all_platforms), GREEN)
                if tile == '2':
                    Wall(self, col, row, (self.deadly_platforms, self.all_platforms), RED)
                if tile == '3':
                    Wall(self, col, row, (self.deadly_platforms, self.shootable_platforms, self.all_platforms), ORANGE)
                if tile == "T":
                    Trigger(self, col, row,(self.all_platforms, self.triggers))
                if tile == "P":
                    self.player = Player(self, col, row)

    def quit(self):
        pg.quit()
        sys.exit()

    def new(self):
        #sprite groups
        self.all_sprites = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.deadly_platforms = pg.sprite.Group()
        self.shootable_platforms = pg.sprite.Group()
        self.triggers = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        #call load data
        self.load_data()
        #create map
        self.create_map(self.map)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        #move the map
        for plat in self.all_platforms:
            plat.rect.x -= self.plat_speed
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
        #if trigger comes on screen, kill it and spawn another card
        for trigger in self.triggers:
            if trigger.rect.x < WIDTH:
                trigger.kill()
                map = Map(path.join(maps_Folder, random.choice(CARD_LIST)))
                self.create_map(map)
        #check for collisions between player and deadly objects / platforms
        hits = pg.sprite.spritecollide(self.player, self.deadly_platforms, False)
        if hits:
            self.playing = False
        #check bullets colliding with shootable platforms
        hits = pg.sprite.groupcollide(self.bullets, self.shootable_platforms, True, True)
        # check for bullets colliding with all platforms
        hits = pg.sprite.groupcollide(self.bullets, self.all_platforms, True, False)
        #Update loops
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused

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
        # self.draw_grid()
        #pause screen
        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text('Paused', self.title_font,105, RED, WIDTH / 2, HEIGHT / 2, align='center')
        #after drawing, flip display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(skyBlue)
        self.draw_text(TITLE, self.title_font, 150, BLACK, WIDTH / 2, HEIGHT / 4, align='center')
        self.draw_text("Arrows to move and jump",self.title_font, 40, GRAY, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text("Press 1 for Normal, 2 for Hard, 3 for Extra Hard",self.title_font, 40, GRAY, WIDTH / 2, HEIGHT * 3 / 4, align='center')
        pg.display.flip()
        self.waitForKey()

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(skyBlue)
        self.draw_text("GAME OVER", self.title_font, 125, RED, WIDTH / 2, HEIGHT / 4, align='center')
        self.draw_text("Press 1 for Normal, 2 for Hard, 3 for Extra Hard",self.title_font, 40, GRAY, WIDTH / 2, HEIGHT * 3 / 4, align='center')
        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_1:
                        self.plat_speed = PLATFORM_SPEED
                        waiting = False
                    if event.key == pg.K_2:
                        self.plat_speed = PLATFORM_SPEED * 2
                        waiting = False
                    if event.key == pg.K_3:
                        self.plat_speed = PLATFORM_SPEED * 2.5
                        waiting = False

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()