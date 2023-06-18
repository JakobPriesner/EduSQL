from abc import ABC, abstractmethod
from typing import TypeVar, Generic

U = TypeVar('U')


class ICommand(Generic[U], ABC):
    @abstractmethod
    async def handle(self, **kwargs) -> U:
        ...
