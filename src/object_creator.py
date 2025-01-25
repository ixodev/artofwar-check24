from fxmanager import FXManager
from entity import *
from player import Player
from character import Character
from monster import Monster
from boss import Boss
from fx import *
from ipp_interpreter import*
from asset_manager import ASSET_MANAGER


COLLISION_ID = "col_"
SWITCH_MAP_AREA_ID = "map_"
SPAWN_POINT_ID = "spn_"
SPAWN_FX_ID = "sfx_"
SPAWN_CHARACTER_ID = "chr_"
SPAWN_MONSTER_ID = "mtr_"
SPAWN_BOSS_ID = "bss_"
IPP_FILEDEF = "ipp_"
PROCEDURE_DEF = "prc_"


def create_collision(game_map, obj):
    game_map.walls.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))

def create_map_switch(game_map, obj):
    game_map.switch_map_areas.update({(obj.x, obj.y, obj.width, obj.height): obj.name.split('_')[1]})

def create_spawn_point(game_map, obj):
    game_map.spawn_points.update({obj.name.split('_')[1]: (obj.x, obj.y, 0, 0)})

def create_fx(game_map, obj):
    tokens = obj.name.split('_')

    if tokens[3] == "DEFAULT":
        update_rate = DEFAULT_UPDATE_RATE
    else:
        update_rate = int(tokens[3])

    game_map.fx_manager.start_fx(tokens[1], (obj.x, obj.y), int(tokens[2]), update_rate)

def create_ipp(game_map, obj):
    game_map.ipp_file = obj.name.split('_')[1]
    game_map.ipp_interpreter = IPPInterpreter(ASSET_MANAGER.get_file_path(f"Backgrounds/Worlds/{game_map.ipp_file}"),
                                          game_map.world, game_map.player)

def create_proc(game_map, obj):
    action_point = (
        round(obj.x) - 5, round(obj.y) - 5, 10, 10
    )
    function_name = obj.name.split('_')[1]
    game_map.action_points.update({action_point: function_name})

def create_character(game_map, obj):
    tokens = obj.name.split('_')
    entity_name = tokens[1]
    entity = Character(entity_name, pg.math.Vector2(obj.x, obj.y), obj.name)
    add_entity_ipp_helper(game_map, obj, entity, tokens)

def create_monster(game_map, obj):
    tokens = obj.name.split('_')
    entity_name = tokens[1]

    entity = Monster(entity_name, pg.math.Vector2(obj.x, obj.y), game_map.player, obj.name)
    add_entity_ipp_helper(game_map, obj, entity, tokens)

def create_boss(game_map, obj):
    tokens = obj.name.split('_')
    entity_name = tokens[1]

    entity = Boss(entity_name, pg.math.Vector2(obj.x, obj.y), game_map.player, obj.name)
    add_entity_ipp_helper(game_map, obj, entity, tokens)

def add_entity_ipp_helper(game_map, obj, entity, tokens):
    if len(tokens) >= 3:
        game_map.entity_ipp_functions.update({entity: tokens[2]})

    if len(tokens) >= 4:
        layer = int(tokens[3])
    else:
        layer = 1

    game_map.add_entity(entity, layer)

object_creation_functions = {
    COLLISION_ID: create_collision,
    SWITCH_MAP_AREA_ID: create_map_switch,
    SPAWN_POINT_ID: create_spawn_point,
    SPAWN_FX_ID: create_fx,
    SPAWN_CHARACTER_ID: create_character,
    SPAWN_MONSTER_ID: create_monster,
    SPAWN_BOSS_ID: create_boss,
    IPP_FILEDEF: create_ipp,
    PROCEDURE_DEF: create_proc
}

