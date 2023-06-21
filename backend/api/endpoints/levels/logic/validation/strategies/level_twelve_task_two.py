from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelTwelveTaskTwoValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        statementOne: str = "SELECT * from location where id = %s;"
        statementTwo: str = "SELECT * from address where id = %s;"
        statementThree: str = "SELECT * from businesshours where id = %s;"
        resultOne: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statementOne, (2, ))
        resultTwo: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statementTwo, (752, ))
        resultThree: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statementThree, (2, ))
        print(resultOne)
        print(resultTwo)
        print(resultThree)

        if not resultOne and not resultTwo and not resultThree:
            return LevelValidationResult(level="12.2", is_valid=True, message="")
        return LevelValidationResult(level="12.2",
                                     is_valid=False,
                                     message="False DailyBusinessHours")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 12 and task_number == 2
