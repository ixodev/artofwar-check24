# DEPRECATED


import pygame as pg

from utils import get_surface
from tile import *

BUILTIN_TILE_SIZE = "bTileSize"
BUILTIN_TILESET_SOURCE = "bTilesetSource"

BUILTIN_WIDTH = "bWidth"
BUILTIN_HEIGHT = "bHeight"



class MappyReader:
    def __init__(self, filepath: str):
        self.tiles = []
        self.tiles_as_string = []
        self.variables = {}
        self.reload(filepath)
        self.read()

    def reload_w_filepath(self):
        self.texture_regions = []
        self.texture = None
        self.tileset_source = ""
        self.tile_size = 0

        self.read()

    def reload(self, filepath: str):
        self.prog_name = filepath
        self.reload_w_filepath()

    def read(self):
        file = open(self.prog_name, 'r')
        lines = file.read().split('\n')
        file.close()

        for line in lines:
            if line != '\n' and line != "\n\n" and line != '' and not line.startswith("//"):
                self.analyze_line(line)

    def load_tiles(self):
        self.tiles = self.get_tiles()

    def analyze_line(self, line: str):
        blocks = []

        if '=' in line:
            blocks = line.split('=')

            if len(blocks) != 2:
                raise IndexError("Fatal error: = operator takes 2 operands!")

            if blocks[0] == BUILTIN_TILE_SIZE:
                self.tile_size = int(blocks[1])
                return
            elif blocks[0] == BUILTIN_TILESET_SOURCE:
                self.tileset_source = blocks[1]
                self.texture = pg.image.load(self.tileset_source)
                return

            else:
                self.variables.update({blocks[0]: [blocks[1], self.tileset_source]})

        if not ',' in line:
            raise SyntaxError("Error: , expected for separating texcoord values")

        if len(blocks) >= 2:
            self.calculate_value(blocks[1].split(','))
        else:
            self.calculate_value(line.split(','))

    def calculate_value(self, values: list):
        if self.texture is None:
            raise SystemExit("Null pointer on texture, cannot get width or height")
        if self.tile_size == 0:
            raise SystemExit("Tile size is null, all texcoords will be multiplied with 0")

        to_append = []

        for value in values:
            if value == BUILTIN_WIDTH or value == BUILTIN_HEIGHT:
                if value == BUILTIN_WIDTH:
                    to_append.append(self.texture.get_width())
                elif value == BUILTIN_HEIGHT:
                    to_append.append(self.texture.get_height())
            elif '-' in value:
                if BUILTIN_WIDTH in value:
                    to_append.append((self.texture.get_width() - int(value.split('-')[1])) * self.tile_size)
                elif BUILTIN_HEIGHT in value:
                    to_append.append((self.texture.get_height() - int(value.split('-')[1])) * self.tile_size)
                else:
                    raise SyntaxError("Fatal error: wrong use of \"-\" operator")
            else:
                to_append.append(int(value) * self.tile_size)

        to_append.append(self.tileset_source)
        self.texture_regions.append(to_append)

    # NOOT changed it with Sorya

    def get_tiles(self):
        tiles = []

        #for texture_region in self.texture_regions:
         #   tile = Tile(get_surface(pg.image.load(texture_region[4]), [texture_region[0], texture_region[1],
          #                                                             texture_region[2], texture_region[3]]), (0, 0),
           #             texture_region[4])
            #tiles.append(tile)

        return tiles

    def get_prog_name(self):
        return self.prog_name

    def get_variables(self):
        return self.variables

    def get_single_variable(self, name: str):
        return self.variables.get(name)

    def get_single_tile(self, name: str):

        if not (name in self.variables.keys()):
            raise KeyError(f"Unknown name: {name}")

        variable = self.variables.get(name)
        values = variable[0].split(',')

        if len(values) != 4:
            raise IndexError("2D texcoords must have 4 components")

        #return Tile(get_surface(pg.image.load(variable[1]),
        #                        [int(values[0]) * self.tile_size, int(values[1]) * self.tile_size,
        #                         int(values[2]) * self.tile_size, int(values[3]) * self.tile_size]),
        #            (0, 0), variable[1])

    def get_single_tile_as_surface(self, name: str):

        if not (name in self.variables.keys()):
            raise KeyError(f"Unknown name: {name}")

        variable = self.variables.get(name)
        values = variable[0].split(',')

        if len(values) != 4:
            raise IndexError("2D texcoords must have 4 components")

        return get_surface(pg.image.load(variable[1]),
                           [int(values[0]) * self.tile_size, int(values[1]) * self.tile_size,
                            int(values[2]) * self.tile_size, int(values[3]) * self.tile_size])

    def get_single_tile_by_texcoords(self, texcoords: str, tileset_source: str):
        coords = texcoords.split(',')

        if len(coords) != 4:
            raise IndexError("2D texcoords must have 4 components")

        return Tile(get_surface(pg.image.load(tileset_source),
                                [int(coords[0]) * self.tile_size, int(coords[1]) * self.tile_size,
                                 int(coords[2]) * self.tile_size, int(coords[3]) * self.tile_size]), (0, 0),
                    tileset_source)
