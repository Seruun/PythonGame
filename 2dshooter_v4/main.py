# import section
import sys
from os import path
from map import *
import time

# redefined file structure
# !!!! das sprite file war zu groß und unübersichtlich deswegen hab ich es aufgeteilt !!!!
from sprites.ControlBox import *
from sprites.Gate import *
from sprites.Background import *
from sprites.Tree import *
from sprites.ActionArea import *
from sprites.WoodBox import *
from sprites.Wall import *
from sprites.Bullet import *
from sprites.Player import *
from sprites.Enemy import *
import pygame as pg

from config import *
import math
from map import *

pg.mixer.pre_init(44100, 16, 2, 4096)


class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE, VERSION)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'img')
        self.sound_folder = path.join(game_folder, 'sounds')
        self.map = Map(path.join(game_folder, 'mapfile.txt'))
        self.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, PLAYER_IMG_SIZE)
        self.enemy_img = pg.image.load(path.join(self.img_folder, ENEMY_IMG)).convert_alpha()
        self.enemy_img = pg.transform.scale(self.enemy_img, ENEMY_IMG_SIZE)

        # load background fx

    def generate_background(self):
        for y in range(0,2500,BACKGROUND_IMG_SIZE[1]):
            for x in range(0,5000,BACKGROUND_IMG_SIZE[0]):
                self.background.append(Background(self, self.img_folder + "/" + BACKGROUND_IMG, [x, y]))

    def initialize(self):
        # initialize all variables and do all the setup for a new game
        EnemyNum = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gates = pg.sprite.Group()
        self.action_area = pg.sprite.Group()
        self.destroyable_objects = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.background = []
        self.player_dead = False
        self.camera = Camera(self.map.width, self.map.height)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'S':
                    self.player = Player(self, col, row, self.camera)
                if tile == 'W':
                    self.woodbox = WoodBox(self, col, row)
                if tile == 'T':
                    self.tree = Tree(self,col,row)
                if tile == 'G':
                    self.gate = Gate(self,col,row)
                if tile == 'A':
                    self.a_area = ActionArea(self, col, row)
                if tile == 'C':
                    self.control_box = ControlBox(self, col, row)
                if tile == 'E':
                    EnemyNum += 1
                    self.enemy = Enemy(self, col, row, EnemyNum)

        sound_background = pg.mixer.music.load(self.sound_folder + "/" + SOUND_BACKGROUND)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

    # game loop
    def run(self):
        self.playing = True
        self.playtime_clock = pg.time.Clock()
        self.time_played = 0
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

            #measure time played
            self.playtime_tick = self.playtime_clock.tick()
            self.time_played += self.playtime_tick
            if self.player_dead == True:
                break
        self.show_go_screen()
        self.quit()

    def quit(self):
        pg.quit()
        sys.exit()

    # update - update all values of objects
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.action_area.update()
        self.camera.update(self.player)
        # bullet update

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.screen.blit(self.background.image, self.background.rect)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet(self, self.player)

    def show_start_screen(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
                
        self.screen.fill(WHITE)


    def show_go_screen(self):
        myfont = pg.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Game Over', False, (0, 0, 0))
        self.screen.blit(textsurface,(0,0))
        print("Playtime: " + str(self.time_played / 1000) + " seconds")
        time.sleep(5)



# create the game object
g = Game()
g.show_start_screen()
while True:
    g.initialize()
    g.run()
    g.show_go_screen()
