from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelThreeTaskOneValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        statement: str = "SELECT DBH.starttime as starttime, DBH.endtime as endtime" \
                         "FROM location L " \
                         "JOIN BusinessHours BH ON L.businesshours_id = BH.id " \
                         "JOIN DailyBusinessHours DBH ON BH.monday_id = DBH.id " \
                         "WHERE L.id = %s;"
        result: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement, (2,))
        answer_times: list[str] = payload["answer"].split("-")
        if result["starttime"] != answer_times[0] or result["endtime"] != answer_times[1]:
            return LevelValidationResult(level="3.1",
                                         is_valid=False,
                                         message="False DailyBusinessHours")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 3 and task_number == 1
