import os
import pygame as pg

from fx import FX
from asset_manager import AssetManager
from read_meta import read_meta_file


class FXManager:
    def __init__(self, game_map):
        self.game_map = game_map
        self.asset_manager = AssetManager()
        self.all_fx = {}
        self.current_fxs = []
        self.read()

    def read(self):
        file = f"{self.asset_manager.assets_dir}/FX/all_fx.meta"
        self.all_fx = read_meta_file(file)

    def get_fx_size(self, name: str):
        arr = self.all_fx[f"{name}Size"]
        arr[0] = int(arr[0])
        arr[1] = int(arr[1])
        return arr

    def start_fx(self, name: str, pos: tuple, loop: int, update_rate: int):
        size = self.all_fx.get(f"{name}Size")
        size[0] = int(size[0])
        size[1] = int(size[1])
        fx = FX(name, size, pos, loop, update_rate)
        fx.start()

        self.game_map.group.add_internal(fx, 6)
        self.current_fxs.append(fx)


    def update(self):
        for fx in self.current_fxs:
            if not fx.running:
                self.current_fxs.remove(fx)
                self.game_map.group.remove_internal(fx)
