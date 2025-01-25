import os
import random
import sys

import pygame as pg
import pytmx
import pyscroll

from object_creator import *
from asset_manager import AssetManager
from read_meta import read_meta_file
from game_map import *
from player import Player
from monster import Monster
from game_settings import *
from entity_manager import *
from hud import *


AMAZON_COLOR = (59, 122, 87)


class World:
    def __init__(self, id: int, screen: pg.Surface, game):
        self.asset_manager = AssetManager()

        self.id = id
        self.screen = screen
        self.player = Player(pg.math.Vector2(0, 0))

        self.sprite_group = pg.sprite.Group()
        self.entity_manager = EntityManager(self)
        self.game = game
        self.maps = {}
        self.load_maps()
        self.trig_map_switch_effect = False
        self.map_switch_effect_rect = pg.Rect(0, self.screen.get_height() * -1, self.screen.get_width(), self.screen.get_height())

    def load_maps(self):

        self.world_properties = read_meta_file(self.asset_manager.get_world_meta_file(self.id))
        self.maps_as_strings = self.world_properties.get("maps")


        for map_as_string in self.maps_as_strings:
            map_path = self.asset_manager.get_map_path(map_as_string)
            self.maps.update({map_path: GameMap(map_path, self.screen, self.player, self, self.game)})


        if not "main_map" in self.world_properties.keys():
            raise Exception("Cannot find main map to load")


        self.main_map = GameMap(self.asset_manager.get_map_path(self.world_properties.get("main_map")), self.screen, self.player, self, self.game)
        obj = self.main_map.tmx_data.get_object_by_name(MAIN_SPAWN_POINT_FULL)
        self.player.position = [obj.x, obj.y]


        self.maps.update({self.asset_manager.get_map_path(self.world_properties.get("main_map")): self.main_map})


        self.current_map = self.main_map
        self.previous_map = self.current_map


        if not self.main_map.map_path in self.maps.keys():
            self.maps.update({self.main_map.map_path: self.main_map})


        self.reload_player_position()


    def switch_map(self, file: str):

        if self.maps.get(file) is None:
            self.maps.update({self.asset_manager.get_map_path(file): GameMap(self.asset_manager.get_map_path(file), self.screen, self.player, self, self.game)})


        self.previous_map = self.current_map
        self.current_map = self.maps.get(self.asset_manager.get_map_path(file))

        self.reload_player_position()
        self.current_map.group.center(self.player.rect.center)
        self.previous_map.group.center(self.player.rect.center)
        self.trig_map_switch_effect = True

    def reload_player_position(self):
        if self.current_map is self.main_map:
            obj = self.current_map.tmx_data.get_object_by_name(MAIN_SPAWN_POINT_FULL)
        else:
            obj = self.current_map.tmx_data.get_object_by_name(SPAWN_POINT_ID + self.previous_map.filename)
        self.player.position = [obj.x, obj.y]


    def update(self, pressed_keys: list, action_keys: dict):
        self.current_map.update(pressed_keys, action_keys)

        if self.current_map.map_to_switch_to is not None:
            file = self.current_map.map_to_switch_to
            self.current_map.map_to_switch_to = None
            self.switch_map(file)

        if not self.trig_map_switch_effect:
            self.sprite_group.update()

    def make_map_switch_effect(self):
        self.map_switch_effect_rect.y += 50
        if self.map_switch_effect_rect.y < 0:
            self.previous_map.draw()

        pg.draw.rect(self.screen, pg.Color(AMAZON_COLOR), self.map_switch_effect_rect)

        if self.map_switch_effect_rect.y >= self.screen.get_height():
            self.trig_map_switch_effect = False
            self.map_switch_effect_rect.y = self.screen.get_height() * -1



    def draw(self):
        self.current_map.draw()

        if self.trig_map_switch_effect:
            self.make_map_switch_effect()

        blit_handle_text(self.screen, self.current_map.draw_help_text)