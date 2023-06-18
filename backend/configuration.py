from dotenv import load_dotenv
from injector import Module, singleton, Injector

from database.database_extension import add_database
from log.logger_extension import add_logger
from mediator.mediator_extension import add_mediator


class Configuration(Module):
    def configure(self, binder):
        load_dotenv()
        binder.bind(Injector, binder, scope=singleton)
        add_logger(binder)
        add_mediator(binder)
        add_database(binder)
