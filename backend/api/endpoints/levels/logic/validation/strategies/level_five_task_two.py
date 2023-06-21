from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelFiveTaskTwoValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        statement: str = """
SELECT 1 as Exists
FROM pg_roles AS r 
JOIN pg_auth_members AS am ON am.member = r.oid 
JOIN pg_roles AS r2 ON am.roleid = r2.oid 
WHERE r.rolname = %s AND r2.rolname = %s;
"""
        person_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                               (user_uuid, "professor"))
        if person_in_db["exists"] != 1:
            return LevelValidationResult(level="5.2",
                                         is_valid=False,
                                         message=f"User \"{user_uuid}\" has not the role \"professor\".")
        return LevelValidationResult(level="5.2", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 5 and task_number == 2
