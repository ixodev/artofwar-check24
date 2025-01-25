from task import *

class TaskManager:
    def __init__(self, game):
        self.game = game
        self.world = self.game.world

        self.__tasks = { }
        self.__tasks_queue = []

    def get_tasks(self):
        return self.__tasks