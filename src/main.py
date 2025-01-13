"""

Art Of War v0.1.0, a 2D Open-World, Retro-Style RPG written by ixodev (http://www.ixodev.github.io).
Powered by Python 3.10 & Pygame 2.4.0, (SDL 2.26.4)

Use is subject to license terms. Please see the LICENSE file located in the parent directory.
Copyright (c) Younes Bendimerad <alias ixodev>, 2024, Munich, Germany.

THIS IS A SOURCE FILE. DO NOT EDIT PLEASE!

"""



import pygame as pg
import sys


pg.init()
pg.display.init()
pg.font.init()
pg.mixer.init()

from game import *
from software_updates_checker import *



if __name__ == "__main__":

    check_software_updates()

    app = Game()

    app.run()

    pg.quit()
    sys.exit(0)

