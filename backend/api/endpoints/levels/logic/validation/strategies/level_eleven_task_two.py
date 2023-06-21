from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelElevenTaskTwoValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        statement: str = "SELECT grade from examattempt ORDER BY id LIMIT 1;"
        result: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement)
        if result["grade"] != 1.7:
            message = "The grade of the ExamAttempt with the lowest ID was not adjusted to 1.7."
            return LevelValidationResult(level="11.2", is_valid=False, message=message)
        return LevelValidationResult(level="11.2", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 2 and task_number == 3
