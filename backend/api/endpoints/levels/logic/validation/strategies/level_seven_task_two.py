from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelSevenTaskTwoValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")
        self.expected_name: str = "Language Skills"
        self.expected_description: str = "Good english skills"
        self.expected_restriction_id = "";

    async def handle(self, user_uuid: str) -> LevelValidationResult:
        statement: str = "SELECT * FROM Restriction WHERE Name = %s AND Description = %s;"
        restriction_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                 (self.expected_name, self.expected_description))
        if not restriction_in_db:
            return LevelValidationResult(level="7.2",
                                         is_valid=False,
                                         message=f"Restriction \"{self.expected_name} - {self.expected_description}\" does not exist in the Table \"Restriction\".")
        self.expected_restriction_id = restriction_in_db["Id"]
        statement: str = "SELECT * FROM LectureToRestriction WHERE RestrictionId = %s;"
        lecture_to_restriction_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                    (self.expected_restriction_id))
        if not lecture_to_restriction_in_db:
            return LevelValidationResult(level="7.2",
                                         is_valid=False,
                                         message=f"Linkage between Lecture and Restriction \"{self.expected_name}, {self.expected_restriction_id}\" does not exist in the Table \"LectureToRestriction\".")
        return LevelValidationResult(level="7.2",
                                     is_valid=True,
                                     message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 7 and task_number == 2
