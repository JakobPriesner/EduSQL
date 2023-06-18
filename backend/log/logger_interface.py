from logging import Logger, NOTSET
from abc import ABC


class ILogger(ABC, Logger):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
    ...
