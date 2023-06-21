from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelSixTaskThreeValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        stmt: str = "SELECT id FROM person " \
                    "WHERE firstname = %s And lastname = %s;"
        db_res: dict = await self._db.load_single_by_sql(self._db_user_handler.get_user_by_username("admin"),
                                                            user_uuid, stmt, (payload["firstname"], payload["lastname"]))
        person_id: str = db_res["id"]
        statement: str = "SELECT count(*) FROM person " \
                         "JOIN persontopermission ptp on id=ptp.personid " \
                         "JOIN permission p on ptp.permissionid=p.id " \
                         "JOIN roomrequiredpermission r on ptp.permissionid = r.permissionid " \
                         "WHERE person.id = %s AND r.roomname = 'H.1.1';"
        db_result: dict = await self._db.load_single_by_sql(self._db_user_handler.get_user_by_username("admin"),
                                                            user_uuid, statement, (person_id,))
        if db_result["count"] < 1:
            return LevelValidationResult(level="6.3",
                                         is_valid=False,
                                         message="")
        return LevelValidationResult(level="6.3", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 6 and task_number == 1
