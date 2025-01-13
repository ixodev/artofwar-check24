import pygame as pg
import pytmx
import pyscroll

from game_settings import *
from asset_manager import AssetManager
from fxmanager import FXManager

from entity import *
from player import Player
from character import Character
from monster import Monster
from boss import Boss
from fx import *

from giant_racoon import GiantRacoon
from i_interpreter import IPPInterpreter
from hud import *


ZOOM = 3

COLLISION_ID = "c"
SWITCH_MAP_AREA_ID = "m_"
SPAWN_POINT_ID = "s_"
MAIN_SPAWN_POINT_FULL = "s_main"
SPAWN_FX_ID = "fx_"

SPAWN_CHARACTER_ID = "ec_"
SPAWN_MONSTER_ID = "em_"
SPAWN_BOSS_ID = "eb_"

PLAYER_LAYER = 3
IPP_FILEDEF = "ipp_"


class GameMap:
    def __init__(self, map_path: str, screen: pg.Surface, player: Player, world, game):
        self.screen = screen
        self.asset_manager = AssetManager()
        self.player = player
        self.player_last_actual_position = self.player.position.copy()
        self.map_path = map_path
        self.filename = self.map_path.split('/')[-1]
        self.world = world
        self.game = game

        self.tmx_data = pytmx.util_pygame.load_pygame(map_path)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = TEXTURE_SCALING
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        self.entities = []
        self.group.add_internal(self.player, PLAYER_LAYER)
        self.walls = []
        self.switch_map_areas = {}

        self.spawn_points = {}
        self.main_spawn_point = ()

        self.map_to_switch_to = None
        self.fx_manager = FXManager(self)

        self.ipp_file = ""
        #self.ipp_interpreter = IPPInterpreter()
        self.entity_ipp_functions = {}

        self.create_objects()

        self.is_interaction = False
        self.draw_help_text = "Press Space to enter a house or to interact"

    def add_entity(self, entity: Entity, layer: int = 1):
        self.group.add_internal(entity, layer)
        #self.group.add_internal(entity.weapon, 1)
        self.entities.append(entity)
        self.world.entity_manager.add_entity(entity)

    def create_objects(self):
        self.walls.clear()

        for obj in self.tmx_data.objects:
            if obj.name.startswith(COLLISION_ID):
                self.walls.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == MAIN_SPAWN_POINT_FULL:
                self.main_spawn_point = (obj.x, obj.y)
            elif obj.name.startswith(SWITCH_MAP_AREA_ID):
                self.switch_map_areas.update({(obj.x, obj.y, obj.width, obj.height): obj.name.split('_')[1]})
            elif obj.name.startswith(SPAWN_POINT_ID):
                self.spawn_points.update({obj.name.split('_')[1]: (obj.x, obj.y, 0, 0)})
            elif obj.name.startswith(SPAWN_FX_ID):
                tokens = obj.name.split('_')

                if tokens[3] == "DEFAULT":
                    update_rate = DEFAULT_UPDATE_RATE
                else:
                    update_rate = int(tokens[3])

                self.fx_manager.start_fx(tokens[1], (obj.x, obj.y), int(tokens[2]), update_rate)
            elif obj.name.startswith(IPP_FILEDEF):
                self.ipp_file = obj.name.split('_')[1]
                self.ipp_interpreter = IPPInterpreter(self.asset_manager.get_file_path(f"Backgrounds/Worlds/{self.ipp_file}"), self.world, self.player)

            else:
                tokens = obj.name.split('_')
                entity_name = tokens[1]

                if obj.name.startswith(SPAWN_CHARACTER_ID):
                    entity = Character(entity_name, pg.math.Vector2(obj.x, obj.y), obj.name)
                elif obj.name.startswith(SPAWN_MONSTER_ID):
                    entity = Monster(entity_name, pg.math.Vector2(obj.x, obj.y), self.player, obj.name)
                elif obj.name.startswith(SPAWN_BOSS_ID):
                    #entity = GiantRacoon(entity_name, pg.math.Vector2(obj.x, obj.y), self.player, obj.name)
                    entity = Boss(entity_name, pg.math.Vector2(obj.x, obj.y), self.player, obj.name)
                
                if len(tokens) >= 3:
                    self.entity_ipp_functions.update({entity: tokens[2]})

                if len(tokens) >= 4:
                    layer = int(tokens[3])
                else:
                    layer = 1

                self.add_entity(entity, layer)

    def update(self, pressed_keys: list, action_keys: dict):
        map_switch_string = self.check_map_switches(action_keys)
        self.fx_manager.update()
        self.group.update()
        self.check_collisions(pressed_keys, action_keys)

        if not self.player.wait_moving:
            self.group.center(self.player.rect.center)


        if map_switch_string is not None:
            self.map_to_switch_to = map_switch_string
        else:
            self.map_to_switch_to = None


    def draw(self):
        self.group.draw(self.screen)


    def check_collisions(self, pressed_keys: list, action_keys: dict):
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()
            self.player.wait_moving = True

        for sprite in self.entities:
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
            if self.player.rect.colliderect(sprite.rect):
                if action_keys[pg.K_SPACE] and self.is_interaction == False:
                    self.world.entity_manager.inc_interactions(sprite.id)
                    self.is_interaction = True
                    if sprite in self.entity_ipp_functions:
                        self.ipp_interpreter.exec_function(self.entity_ipp_functions[sprite], [sprite])

                else:
                    self.is_interaction = False
            else:
                self.is_interaction = False
                

    def check_map_switches(self, action_keys: dict):
        if action_keys[pg.K_SPACE]:
            for switch_area in self.switch_map_areas.keys():
                if self.player.feet.colliderect(pg.Rect(switch_area[0], switch_area[1], switch_area[2], switch_area[3])):
                    return self.switch_map_areas.get(switch_area)


        return None

    def __repr__(self):
        return f"GameMap (game_map.py), filename: {self.filename}"

