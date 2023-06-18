from abc import ABC, abstractmethod
from typing import Type

from command_interface import ICommand


class IMediator(ABC):
    @abstractmethod
    async def execute_async(self, command: Type[ICommand], **kwargs) -> any:
        ...
