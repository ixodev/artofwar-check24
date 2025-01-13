import random

import pygame as pg
from boss import Boss
from player import Player
from utils import *


VEL = 8
ATTACK_RELOAD = 15


class GiantRacoon(Boss):
    def __init__(self, name: str, pos: pg.math.Vector2, player: Player, id: str):
        super().__init__(name, pos, player, id)

        self.states = {
            "idle": False,
            "charge": False,
            "attack": False,
            "jump": False
        }

        self.moves = {
            "left": False,
            "right": False
        }

        self.action("idle")

        self.reload_attack = False
        self.reload_counter = 0

        self.delta_time_limit = 7

    def boss_logic(self):

        center = (self.position[0] + self.w / 2, self.position[1] + self.h / 2)
        player_center = (self.player.position[0] + self.player.w / 2, self.player.position[1] + self.player.h / 2)

        # Charge, then attack
        if get_distance(center[0], player_center[0], center[1], player_center[1]) <= 50 and not self.reload_attack:
            # If the player was just detected, first charge
            if not self.states["charge"] and not self.states["attack"]:
                self.action("charge")
            # If charging is complete, attack
            elif self.states["charge"] and self.animation_ended:
                self.action("attack")
            # If attack is complete, charge to restart again because we are in the condition block where the boss has to attack
            elif self.states["attack"] and self.animation_ended:
                self.reload_attack = True

        else:
            if self.animation_ended:
                self.action("idle", reset_tx=False)

        if self.reload_attack:
            self.reload_counter += 1

            if self.reload_counter == ATTACK_RELOAD:
                self.reload_counter = 0
                self.reload_attack = False

        self.update_moves()

    def update_moves(self):
        if self.states["jump"]:
            # Then the boss has just begun to move because no move direction is activated
            if not self.moves["right"] and not self.moves["left"]:
                self.moves[random.choice(list(self.moves.keys()))] = True


        if self.moves["left"]:
            self.position[0] -= VEL
        else:
            self.position[1] += VEL