TASK_PROPERTIES_IGNORE = 0
TASK_STATE_FINISHED = 1
TASK_STATE_UNFINISHED = 2
TASK_PROPERTIES_ACKNOWLEDGE = 3


class Task:
    def __init__(self, task_manager, state: int = TASK_STATE_UNFINISHED, property: int = TASK_PROPERTIES_IGNORE):
        self.task_manager = task_manager
        self.state = state
        self.property = property

    """ Has to be overloaded """
    def run(self):
        pass