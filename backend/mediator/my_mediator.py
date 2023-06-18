from typing import Type

from injector import Injector, inject

from command_interface import ICommand
from log.logger_interface import ILogger
from mediator.mediator_interface import IMediator


class Mediator(IMediator):
    @inject
    def __init__(self, injector: Injector, logger: ILogger):
        self._injector = injector
        self._logger = logger

    async def execute_async(self, command: Type[ICommand], **kwargs) -> any:
        self._logger.info(f"Executing command \"{command.__name__}\".")
        injected_command: ICommand = self._injector.get(command)
        return await injected_command.handle(**kwargs)
