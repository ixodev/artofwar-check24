import sys
import pygame as pg

from read_meta import *
from game_settings import *
from asset_manager import AssetManager
from utils import get_surface
from spritesheet_entity_handler import SpritesheetEntityHandler
from weapon import Weapon



ANIMATIONS_FILE = "animations.meta"
SCALE = 1
DEFAULT_TIME_COUNTER = 3

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3


""" Base class for all entities """
class Entity(pg.sprite.Sprite):

    """ Constructor initializes entity, loads spritesheets and informations about animations, etc... """
    def __init__(self, name: str, pos: pg.math.Vector2, id: str):
        super().__init__()
        #self.weapon = Weapon("Sword")

        self.asset_manager = AssetManager()
        self.name = name  # Directory where to find (relative path: ex: assets/Actor/Characters/DarkNinja) here DarkNinja is the name
        self.find_type()  # Type, can be changed
        self.delta_time_counter = 0
        self.delta_time_limit = DEFAULT_TIME_COUNTER

        self.id = id

        self.spritesheet_handler = SpritesheetEntityHandler(self)  # Useful class for handling with metadicts (animations)

        self.animations = self.spritesheet_handler.animations  # Then we don't have to write xxx.spritesheet_handler.animations

        self.tx = 0
        self.ty = 0
        self.w = self.spritesheet_handler.sprite_width # Idem
        self.h = self.spritesheet_handler.sprite_height # Idem

        self.current_spritesheet_surface = self.spritesheet_handler.current_surface # Current spritesheet as pg.Surface
        self.current_animation_string = self.spritesheet_handler.current_animation # Current animation string as example "idle" or "special2"

        self.setup(pos) # Setup things

        self.update_trigger = False # Update trigger
        self.moved_back = False

        self.entity_type = "entity"
        self.animation_ended = False

    """ Finds the type of the entity """
    def find_type(self):

        for d in os.listdir(f"{self.asset_manager.assets_dir}/Actor"):
            for d2 in os.listdir(f"{self.asset_manager.assets_dir}/Actor/{d}"):
                if d2 == self.name:
                    self.type = d
                    return
        raise ValueError("Cannot find entity type")

    """ Setup things """
    def setup(self, pos: pg.math.Vector2):

        self.image = get_surface(self.current_spritesheet_surface, [self.tx, self.ty, self.w, self.h]) # Crop image

        self.rect = self.image.get_rect().move(pos) # Get the image's rect

        # Useful for collision detection
        self.position = [pos[0], pos[1]]
        self.old_position = self.position.copy()

        self.feet = pg.Rect(self.rect.x + self.rect.width * 0.125, self.rect.y + (self.rect.height / 3) * 2, self.w, self.h / 3)

    """ Sets current spritesheet """
    def set_animation(self, value: str):
        if value not in self.animations.keys():
            print(f"Error: {self} has no animation \"{value}\"", file=sys.stderr)
            value = DEFAULT_ANIMATION

        self.spritesheet_handler.set_spritesheet(value) # Set spritesheet
        self.current_spritesheet_surface = self.spritesheet_handler.current_surface # as pg.Surface
        self.current_animation_string = self.spritesheet_handler.current_animation # as "idle" or "dead" or "default_animation" for example

    """ Resizes current texture """
    def scale_image(self):
        self.image = pg.transform.scale(self.image, (self.image.get_width() * TEXTURE_SCALING, self.image.get_height() * TEXTURE_SCALING))

    """ Incrementing texture coordinates """
    def inc_texcoords(self, axis: str):
        self.tx = self.tx + self.w if axis == 'x' else self.tx + 0
        self.ty = self.ty + self.h if axis == 'y' else self.ty + 0

        if self.tx >= self.current_spritesheet_surface.get_width():
            self.tx = 0
        elif self.ty >= self.current_spritesheet_surface.get_height():
            self.ty = 0


    def reset_texcoords(self, axis: str):
        self.tx = 0 if axis == 'x' else self.tx
        self.ty = 0 if axis == 'y' else self.ty

    """ Has to call update() method??? """
    def check_delta_time_counter(self):
        self.delta_time_counter = self.delta_time_counter + 1 if self.delta_time_counter < self.delta_time_limit else 0
        self.update_trigger = (self.delta_time_counter == 0)

    """ Save feet location and position and other things """
    def save_location(self):
        self.old_position = self.position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    """ In case of collision """
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.moved_back = True

    def set_current_image(self):
        self.image = get_surface(self.current_spritesheet_surface, [self.tx, self.ty, self.w, self.h])

    def update(self):
        self.check_delta_time_counter()
        self.save_location()

        if self.update_trigger:
            self.update_entity()

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom



    """ This method must be overloaded """
    def update_entity(self):
        ...

    def __repr__(self):
        return f"\n-----------entity---------\ntype: {self.type}\nname: {self.name}\n---------------------------\n"