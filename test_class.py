database = []

class Tasks:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_done = False

    def create_task(self):
        database.append(self)

