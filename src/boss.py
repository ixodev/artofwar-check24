import pygame as pg
from entity import Entity
from player import Player

TIME_COUNTER = 5


class Boss(Entity):
    def __init__(self, name: str, pos: pg.math.Vector2, player: Player, id: str):
        super().__init__(name, pos, id)
        self.player = player
        self.delta_time_limit = TIME_COUNTER

        self.states = {}
        self.animation_ended = False

    def get_current_state(self):
        for key in self.states.keys():
            if self.states.get(key):
                return key

        raise ValueError("Boss must have at least 1 state activated")

    def update_entity(self):
        self.save_location()

        self.inc_texcoords('x')

        if self.tx >= self.image.get_width() - self.w:
            self.animation_ended = True
        else:
            self.animation_ended = False

        self.boss_logic()


        self.set_current_image()



    def action(self, val: str, reset_tx: bool = True):
        if reset_tx:
            self.tx = 0

        self.set_animation(val)

        for key in self.states.keys():
            if key == val:
                self.states[key] = True
            else:
                self.states[key] = False

    def boss_logic(self):
        ...