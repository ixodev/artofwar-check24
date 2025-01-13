# DEPRECATED

import os
import random
import pygame as pg

from game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from mappy_reader import MappyReader
from tile import Tile, SCALE


MAP_STYLES = ["winter", "autumn", "summer", "spring", "desert_1", "desert_2"]

ground_tile_spawn_odds = {
    2: 8,
    3: 4
}


class MapGenerator:
    def __init__(self):
        self.tiles = []

        self.floor_mappy = MappyReader("assets/Backgrounds/Tilesets/Mappys/floor.json")

        #self.nature_mappy = MappyReader("assets/Backgrounds/Tilesets/Mappys/invalid.json")
        #self.house_mappy = MappyReader("assets/Backgrounds/Tilesets/Mappys/house.json")

        self.map_style = random.choice(MAP_STYLES)

        self.generate_floor()

    def generate_floor(self):
        prefix = self.map_style + "_floor_"
        attribs = []

        for x in range(int(WINDOW_WIDTH / self.floor_mappy.tile_size / SCALE)):
            for y in range(int(WINDOW_HEIGHT / self.floor_mappy.tile_size / SCALE)):
                attribs.append([random.choice([key for key in self.floor_mappy.variables.keys() if key.startswith(prefix)]), (x * self.floor_mappy.tile_size * SCALE, y * self.floor_mappy.tile_size * SCALE)])

        for attrib in attribs:
            tile = self.floor_mappy.get_single_tile_as_surface(attrib[0])
            self.tiles.append(Tile(tile, (attrib[1][0], attrib[1][1]), self.floor_mappy.tileset_source))

    def draw(self, screen: pg.Surface):
        for tile in self.tiles:
            tile.draw(screen) # Change