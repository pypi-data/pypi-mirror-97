class TaskPending(Exception):
    ''' Exception raised when the task is pending
    '''

    def __init__(self, task_id):
        self.task_id = task_id

    def __repr__(self):
        return f"Task[task_id:{self.task_id}] is pending"

    def __str__(self):
        return self.__repr__()
