import pygame as pg
import math


def get_surface(surface: pg.Surface, rect: list):
    image = pg.Surface([rect[2], rect[3]])
    image.blit(surface, (0, 0), (rect[0], rect[1], rect[2], rect[3]))
    image.set_colorkey([0, 0, 0])
    return image

def get_distance(x1: int, x2: int, y1: int, y2: int):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))