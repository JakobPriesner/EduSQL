from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelOneTaskFiveValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        first_name: str = payload.get("firstName")
        last_name: str = payload.get("lastName")
        statement: str = "SELECT * FROM person WHERE FirstName = %s AND LastName = %s;"
        person_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                               (first_name, last_name))
        if not person_in_db:
            return LevelValidationResult(level="1.5",
                                         is_valid=False,
                                         message=f"Person \"{first_name} {last_name}\" does not exist in the Table \"Person\".")
        return LevelValidationResult(level="1.5", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 1 and task_number == 5
