from injector import Binder, singleton

from mediator.mediator_interface import IMediator
from mediator.my_mediator import Mediator


def add_mediator(binder: Binder):
    binder.bind(IMediator, Mediator, scope=singleton)
