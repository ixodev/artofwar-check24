import sys
import os

import pygame as pg

from game_settings import *
from asset_manager import AssetManager
from world import World
from dialog_box import *


ACTION_KEYS = [pg.K_SPACE, pg.K_h]


class Game:
    def __init__(self):
        self.init_variables()
        self.init_window()
        self.init_components()

    def init_variables(self):
        self.is_running = True
        

    def init_window(self):
        self.asset_manager = AssetManager()
        pg.mixer_music.load(self.asset_manager.get_file_path("Musics/24 - Final Area.ogg"))
        #pg.mixer_music.play(-1, 0.0, 0)

        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(WINDOW_TITLE)
        pg.display.set_icon(self.asset_manager.get_surface(WINDOW_ICON))

        #.image = self.asset_manager.get_surface("")
        #self.image = pg.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))

    def init_components(self):
        self.world = World(1, self.screen, self)
        self.action_keys = {}
        #self.tutorial = pg.image.load("assets/HUD/Tuto.png")
        #self.tutorial = pg.transform.scale(self.tutorial, (self.tutorial.get_width() * TEXTURE_SCALING, self.tutorial.get_height() * TEXTURE_SCALING))

    def update(self, keys: list, action_keys: dict):
        self.world.update(keys, action_keys)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.world.draw()

    def run(self):
        self.screen.fill(pg.Color("white"))
        pg.display.flip()


        while self.is_running:

            self.action_keys.clear()

            for evt in pg.event.get():
                if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE:
                    self.is_running = False
                if evt.type == pg.KEYDOWN:
                    for key in ACTION_KEYS:
                        if evt.key == key:
                            self.action_keys.update({key: True})
                
            for key in ACTION_KEYS:
                if not key in self.action_keys.keys():
                    self.action_keys.update({key: False})

            keys = pg.key.get_pressed()

            self.update(keys, self.action_keys)
            self.render()

            #if pg.time.get_ticks() <= 5000:
                #self.screen.blit(self.tutorial, (self.screen.get_width() / 4 * 3 - self.tutorial.get_width() / 4, self.screen.get_height() / 4 * 3 - self.tutorial.get_height() / 4))


            pg.display.flip()

            self.clock.tick(FPS)

