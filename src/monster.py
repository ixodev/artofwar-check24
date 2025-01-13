import random
import math

import pygame as pg
from entity import *
from player import Player
from quadratic_moving import QuadraticMoving

VEL = 2
TIME_COUNTER = 5
PLAYER_PURSUIT_LIMIT = 100

class Monster(QuadraticMoving):
    def __init__(self, name: str, pos: pg.Vector2, player: Player, id: str):
        super().__init__(name, pos, id, VEL, 20)
        self.current_animation_string = "default_animation"
        self.position = [pos.x, pos.y]
        self.delta_time_limit = TIME_COUNTER
        self.player_pursuit = 0
        self.player = player

    def update_entity(self):
        self.move()

        self.inc_texcoords("y")

        self.set_current_image()
