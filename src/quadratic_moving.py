import pygame as pg

from entity import Entity


class QuadraticMoving(Entity):
    def __init__(self, name: str, pos: pg.math.Vector2, id: str, vel: int, change_move_limit: int):
        super().__init__(name, pos, id)

        self.vel = vel
        self.change_move_limit = change_move_limit

        self.matrices = (
            (
                            ((1, 0), (3, 0)),
                            ((0, 1), (0, 0)),
                            ((-1, 0), (2, 0)),
                            ((0, -1), (1, 0))
                         ),
                         (
                            ((0, -1), (0, 0)),
                            ((1, 0), (3, 0)),
                            ((0, -1), (1, 0)),
                            ((-1, 0), (2, 0))

                         )
        )


        self.move_matrix = 0

        # By default:
        # start ---------->
        # ^              ||
        # |              ||
        # |              ||
        # |              \/
        # <----------------

        self.current_move = 0
        self.distance = 0


    def switch_matrix(self):
        self.current_move = 0
        self.move_matrix = not self.move_matrix

    def move(self):
        self.position[0] += self.matrices[self.move_matrix][self.current_move][0][0] * self.vel
        self.position[1] += self.matrices[self.move_matrix][self.current_move][0][1] * self.vel

        self.distance += self.vel

        if self.distance >= self.change_move_limit:
            self.distance = 0
            self.current_move += 1

            if self.current_move >= len(self.matrices[self.move_matrix]):
                self.current_move = 0

        self.tx = self.w * self.matrices[self.move_matrix][self.current_move][1][0]
