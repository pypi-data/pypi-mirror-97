import rtablify as r
import importlib


class rtablify:
    def __init__(self):
        self.module = importlib.import_module('createRedditTable')
        self.createRedditTable = self.module.createRedditTable


if __name__ == "__main__":

    pass
