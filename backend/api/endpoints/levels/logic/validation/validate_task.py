from typing import Type

from injector import inject, Injector

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.logic.validation.strategies.level_one_task_one import LevelOneTaskOneValidator
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from command_interface import ICommand
from database.db_user_handler import DbUserHandler
from database.postgresql_connection_interface import IPostgresqlConnection
from log.logger_interface import ILogger


class ValidateTask(ICommand[LevelValidationResult]):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler, injector: Injector, logger: ILogger):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._injector: Injector = injector
        self._logger = logger

    async def handle(self, level_number: int, task_number: int, db: str) -> LevelValidationResult:
        matching_validator: list[Type[IConcreteValidation]] = [validator
                                                               for validator in self._get_all_validator()
                                                               if validator.can_handle(level_number, task_number)]
        if len(matching_validator) == 0:
            error_message: str = f"No validator found for level {level_number} task {task_number}."
            self._logger.info(error_message)
            raise Exception(error_message)

        if len(matching_validator) > 1:
            error_message: str = f"Multiple validators found for level {level_number} task {task_number}."
            self._logger.info(error_message)
            raise Exception(error_message)

        return await self._injector.get(matching_validator[0]).handle(db)

    @staticmethod
    def _get_all_validator() -> list[Type[IConcreteValidation]]:
        return [
            LevelOneTaskOneValidator,
        ]