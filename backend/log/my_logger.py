import logging
from datetime import datetime

from injector import Provider, T, Injector

from log.logger_interface import ILogger


class MyLoggerProvider(Provider):
    def get(self, injector: Injector) -> T:
        class_name = injector._stack[0][0].__name__
        return MyLogger(class_name)


class MyLogger(ILogger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

        self.setLevel(logging.DEBUG)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        self.console_handler.setFormatter(self.console_formatter)
        self.addHandler(self.console_handler)

        log_file = datetime.now().strftime('%Y%m%d%H%M%S.log')
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s',
                                                datefmt='%d/%m/%Y %H:%M:%S')
        self.file_handler.setFormatter(self.file_formatter)
        self.addHandler(self.file_handler)

        self.configure_log_levels()

    def configure_log_levels(self):
        loggers = {
            'aiosqlite': logging.INFO,
            'gtts': logging.INFO,
            'urllib3': logging.INFO,
            'pydub': logging.INFO,
            'telegram': logging.INFO,
            'httpx': logging.INFO,
            'schedule': logging.INFO
        }

        for logger_name, level in loggers.items():
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)
