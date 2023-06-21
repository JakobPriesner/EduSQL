from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelSevenTaskOneValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")
        self.expected_name: str = "IT Security"
        self.expected_description: str = "Aspects of secure systems"
        self.expected_modulenumber: str = "5104211"
        self.expected_required_etcs: str = "125"
        self.expected_earned_etcs: str = "5"
        self.expected_semester: str = "6"
        self.expected_type: str = "FWPM"

    async def handle(self, user_uuid: str) -> LevelValidationResult:
        statement: str = "SELECT * FROM Lecture WHERE Name = %s AND Description = %s AND Modulenumber = %s AND RequiredEtcs = %s AND EarnedEtcs = %s AND Semester = %s AND Type = %s;"
        lecture_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                (self.expected_name, self.expected_description,
                                                                 self.expected_modulenumber, self.expected_required_etcs,
                                                                 self.expected_earned_etcs,
                                                                 self.expected_semester,
                                                                 self.expected_type))
        if not lecture_in_db:
            return LevelValidationResult(level="7.1",
                                         is_valid=False,
                                         message=f"Lecture \"{self.expected_name} - {self.expected_description}, {self.expected_modulenumber}, {self.expected_required_etcs}, {self.expected_earned_etcs}, {self.expected_semester}, {self.expected_type}\" does not exist in the Table \"Lecture\".")
        return LevelValidationResult(level="7.1",
                                     is_valid=True,
                                     message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 7 and task_number == 1
