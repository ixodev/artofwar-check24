import pygame as pg

from character import *
from weapon import Weapon


PLAYER_NAME = "Inspector"
VEL = 3
WAIT_MOVING_DELAY = 3

move_indexes = {
    pg.K_s: [0, 'y', 1, DOWN],
    pg.K_w: [1, 'y', -1, UP],
    pg.K_a: [2, 'x', -1, LEFT],
    pg.K_d: [3, 'x', 1, RIGHT],
    pg.K_z: [1, 'y', -1, UP],
    pg.K_q: [2, 'x', -1, LEFT],
}

PLAYER_ID = "ec_Player"

class Player(Character):
    def __init__(self, pos: pg.math.Vector2):
        super().__init__(PLAYER_NAME, pos, PLAYER_ID)
        self.direction = DOWN

        self.rect.center = pos

        self.entity_type = "player"
        self.wait_moving = False
        self.wait_moving_inc = 0

        #self.weapon = Weapon("Sword")
        self.attack = False

    def handle_inputs(self):
        self.set_weapon_pos()

        keys = pg.key.get_pressed()

        if self.wait_moving:
            self.wait_moving_inc += 1

            if self.wait_moving_inc == WAIT_MOVING_DELAY:
                self.wait_moving = False
                self.wait_moving_inc = 0

        for key in move_indexes.keys():
            if keys[key] and not self.wait_moving and not self.attack:
                self.direction = move_indexes.get(key)[3]
                self.tx = move_indexes.get(key)[0] * self.w
                self.is_moving = True
                self.set_animation("walk")

                if move_indexes.get(key)[1] == 'x':
                    self.position[0] += VEL * move_indexes.get(key)[2]
                else:
                    self.position[1] += VEL * move_indexes.get(key)[2]


                return

        self.is_moving = False
        self.set_animation("idle")

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self.position[0], self.position[1]))

    def set_weapon_pos(self):
        ...
        #if self.direction == DOWN:
         #   self.weapon.rect.midtop = (self.position[0], self.position[1] + self.h / 2)
        #elif self.direction == UP:
         #   self.weapon.rect.midtop = self.rect.topleft