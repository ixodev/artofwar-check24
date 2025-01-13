import pygame as pg
from entity import Entity


class EntityManager:
    def __init__(self, world):
        self.entities = {}

    def add_entity(self, entity: Entity):
        self.entities.update({entity.id: 0})

    def inc_interactions(self, id: str):
        n = self.entities[id] + 1
        self.entities.update({id: n})

    def get_interactions(self, id: str):
        return self.entities[id]