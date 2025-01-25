import pytmx
import pyscroll

from ipp_interpreter import IPPInterpreter
from src.object_creator import *


ZOOM = 3
PLAYER_LAYER = 3
MAIN_SPAWN_POINT_FULL = "spn_main"





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
        self.ipp_interpreter = None
        self.entity_ipp_functions = {}
        self.action_points = {}

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

            object_creation_functions[obj.name.split('_')[0] + '_'](self, obj)


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

        for action_point in self.action_points:
            if self.player.rect.colliderect(action_point) and action_keys[pg.K_SPACE]:
                self.ipp_interpreter.exec_function(self.action_points[action_point], [])
                

    def check_map_switches(self, action_keys: dict):
        if action_keys[pg.K_SPACE]:
            for switch_area in self.switch_map_areas.keys():
                if self.player.feet.colliderect(pg.Rect(switch_area[0], switch_area[1], switch_area[2], switch_area[3])):
                    return self.switch_map_areas.get(switch_area)


        return None

    def __repr__(self):
        return f"GameMap (game_map.py), filename: {self.filename}"

