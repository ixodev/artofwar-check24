import pygame as pg


SCALE = 3



class Tile(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, pos: tuple, spritesheet: str):
        super().__init__()

        self.spritesheet = spritesheet

        self.image = pg.transform.scale(image, (image.get_width() * SCALE, image.get_height() * SCALE))
        self.rect = self.image.get_rect().move(pos[0], pos[1]).move(pos[0], pos[1])

    def is_collision(self, sprite: pg.sprite.Sprite):
        ...

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)

