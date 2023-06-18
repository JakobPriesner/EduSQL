from abc import ABC, abstractmethod

from api.endpoints.levels.models.level_validation_result import LevelValidationResult


class IConcreteValidation(ABC):
    @abstractmethod
    async def handle(self, user_uuid: str) -> LevelValidationResult:
        ...

    @classmethod
    @abstractmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        ...
