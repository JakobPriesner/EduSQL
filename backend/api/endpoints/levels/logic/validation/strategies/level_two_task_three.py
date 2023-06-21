from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelTwoTaskThreeValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        statement: str = "SELECT count(*) FROM staff WHERE stafftype = %s;"
        result: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement, ('Professor',))
        if result["count"] != payload["answer"]:
            message = "The amount of Professors was not correct. "
            if result["count"] > payload["answer"]:
                message += "The guessed amount is to low."
            else:
                message += "The guessed amount is to high."
            return LevelValidationResult(level="2.3", is_valid=False, message=message)
        return LevelValidationResult(level="2.3", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 2 and task_number == 3
