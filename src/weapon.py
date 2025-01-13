import pygame as pg

from asset_manager import AssetManager

DEFAULT_IMG = "Sprite.png"
IN_HAND_IMG = "SpriteInHand.png"

SCALE = 3
DAMAGE = 10

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3


class Weapon(pg.sprite.Sprite):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

        self.asset_manager = AssetManager()

        img1 = self.asset_manager.get_surface(f"Items/Weapons/{self.name}/{DEFAULT_IMG}")
        img2 = self.asset_manager.get_surface(f"Items/Weapons/{self.name}/{IN_HAND_IMG}")

        self.images = [img1, img2]

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.damage = DAMAGE
        self.use = 0

        self.direction = UP

    def switch_image(self):
        self.image = self.images[self.images.index(self.image) - 1]

    def set_direction(self, direction: int):
        self.direction = direction
        self.set_rotation()

    def set_rotation(self):

        if self.direction == DOWN:
            self.image = self.images[1]
        elif self.direction == UP:
            self.image = pg.transform.rotate(self.images[1], 180)
        elif self.direction == LEFT:
            self.image = pg.transform.rotate(self.images[1], -90)
        else:
            self.image = pg.transform.rotate(self.images[1], 90)

    def update(self):
        ...

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)
