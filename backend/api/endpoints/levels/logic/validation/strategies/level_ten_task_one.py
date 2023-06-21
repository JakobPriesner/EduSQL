from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelTenTaskOneValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        payload: dict = kwargs.get("payload")
        matriculation_number: int = payload.get("matriculationNumber")
        average_grade: float = payload.get("averageGrade")
        statement: str = """
SELECT s.MatriculationNumber as MatNumber, AVG(e.Grade) AS GradeAverage
FROM Student s
JOIN ExamAttempt e ON s.MatriculationNumber = e.StudentMatriculationNumber
GROUP BY s.MatriculationNumber
ORDER BY GradeAverage ASC
LIMIT 1;
"""
        result: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement)
        if not result["matnumber"] == matriculation_number or not result["gradeaverage"] == average_grade:
            return LevelValidationResult(level="10.1",
                                         is_valid=False,
                                         message=f"Invalid Matriculation Number or Average Grade was provided.")
        return LevelValidationResult(level="10.1", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 10 and task_number == 1



