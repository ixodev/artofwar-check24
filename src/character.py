import pygame as pg

from utils import get_surface
from entity import Entity


TIME_COUNTER = 4

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3

class Character(Entity):
    def __init__(self, name: str, pos: pg.math.Vector2, id: str):
        super().__init__(name, pos, id)
        self.entity_type = "character"
        self.wait_moving = False
        self.delta_time_limit = TIME_COUNTER

    def handle_inputs(self):
        ...

    def update_entity(self):




        self.handle_inputs()

        if not self.wait_moving:
            self.inc_texcoords('y')
            self.set_current_image()


        #if self.entity_type != "player":
         #   self.scale_image()