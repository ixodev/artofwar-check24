import pygame as pg
from asset_manager import AssetManager
from utils import get_surface


DEFAULT_UPDATE_RATE = 1


class FX(pg.sprite.Sprite):
    def __init__(self, name: str, sprite_size: tuple, pos: tuple, loop: int, update_rate: 5):
        super().__init__()

        self.name = name
        self.size = sprite_size
        self.loop = loop
        self.counter = 1
        self.update_rate = update_rate
        self.update_counter = 1

        self.tx = 0
        self.ty = 0

        self.running = False

        self.asset_manager = AssetManager()

        self.spritesheet = self.asset_manager.get_surface(f"FX/{self.name}.png")
        self.image = get_surface(self.spritesheet, [self.tx, self.ty, self.size[0], self.size[1]])
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def start(self):
        self.running = True

    def update(self):
        if self.update_counter != self.update_rate:
            self.update_counter += 1
        
        else:
            self.update_counter = 0
            self.tx += self.size[0]

            if self.tx >= self.spritesheet.get_width():
                self.tx = 0
                
                if self.loop != -1:
                    self.counter += 1

                    if self.counter == self.loop + 1:
                        self.running = False        

            self.image = get_surface(self.spritesheet, [self.tx, self.ty, self.size[0], self.size[1]])