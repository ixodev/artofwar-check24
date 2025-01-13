import pygame as pg
import os



ASSETS_DIR_PATH_TESTER = "assets_dir_path_tester"

class AssetManager:
    def __init__(self):
        self.path_prefix = ""

        if not os.path.isfile(f"assets/{ASSETS_DIR_PATH_TESTER}"):
            self.path_prefix = "../"
            if not os.path.isfile(f"{self.path_prefix}assets/{ASSETS_DIR_PATH_TESTER}"):
                raise IOError("Cannot find assets_dir_path_tester, exiting.")
            
        self.assets_dir = f"{self.path_prefix}assets"

    def get_surface(self, path: str):
        return pg.image.load(f"{self.assets_dir}/{path}" if not path.startswith('/') else f"{self.assets_dir}{path}")

    def get_world_meta_file(self, id: int):
        return f"{self.assets_dir}/Backgrounds/Worlds/world-{id}.meta"

    def get_map_path(self, name: str):
        return f"{self.assets_dir}/Backgrounds/Worlds/{name}"

    def get_entity_surface(self, file: str, entity_type: str, entity_name: str):
        return pg.image.load(f"{self.assets_dir}/Actor/{entity_type}/{entity_name}/{file}" if not file.startswith('/') else f"{self.assets_dir}/Actor/{entity_type}/{entity_name}{file}")
     
    def get_entity_anim_meta_file(self, entity_type: str, entity_name: str):
        return f"{self.assets_dir}/Actor/{entity_type}/{entity_name}/spritesheets.meta"

    def get_file_path(self, path: str):
        return f"{self.assets_dir}{path}" if path.startswith('/') else f"{self.assets_dir}/{path}"