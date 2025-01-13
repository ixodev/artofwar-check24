import pygame as pg
from game_map import GameMap
from player import Player


class Arena(GameMap):
    def __init__(self, map_path: str, screen: pg.Surface, player: Player):
        super().__init__(map_path, screen, player)
        ...

    def start_fight(self):
        ...