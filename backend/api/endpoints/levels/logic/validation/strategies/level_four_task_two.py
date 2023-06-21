from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelFourTaskTwoValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        statement: str = "SELECT A.addressaddition as name " \
                         "FROM Location L " \
                         "JOIN Address A ON L.addressid = a.id " \
                         "WHERE L.library = true;"
        result: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement)

        if result.get('name') != payload.get('answer')[0]:
            return LevelValidationResult(level="4.2",
                                         is_valid=False,
                                         message="False Locations")
        return LevelValidationResult(level="4.2", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 4 and task_number == 2
