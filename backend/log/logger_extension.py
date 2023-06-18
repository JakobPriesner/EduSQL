from injector import Binder, Provider

from log.logger_interface import ILogger
from log.my_logger import MyLoggerProvider


def add_logger(binder: Binder) -> None:
    binder.bind(ILogger, MyLoggerProvider())
