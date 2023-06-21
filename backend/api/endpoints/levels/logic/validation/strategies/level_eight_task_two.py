from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelEightTaskTwoValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")
        self.expected_exam_id: str = ""
        self.expected_student_matriculation_number_1: str = "3000718"
        self.expected_student_matriculation_number_2: str = "4005213"
        self.expected_student_matriculation_number_3: str = "5002417"
        self.expected_room_name: str = "H.1.1"
        self.expected_score_1: str = "100"
        self.expected_score_2: str = "110"
        self.expected_score_3: str = "60"
        self.expected_grade_1: str = "1.7"
        self.expected_grade_2: str = "1.3"
        self.expected_grade_3: str = "4.0"
        self.expected_written_in_semester: str = "6"
        self.expected_duration_in_minutes: str = "90"
        self.expected_start_time_stamp: str = "2023-07-14T10:00:00"
        self.expected_end_time_stamp: str = "2023-07-14T11:30:00"
        self.expected_exam_type: str = "Written"
        self.expected_scanned_at: str = "2023-07-14T09:50:00"

    async def handle(self, user_uuid: str) -> LevelValidationResult:
        statement: str = "SELECT * FROM ExamAttempt WHERE ExamId = %s AND StudentMatriculationnumber = %s AND RoomName = %s AND Score = %s AND Grade = %s AND WrittenInSemester = %s AND DurationInMinutes = %s AND StartTimeStamp = %s AND EndTimeStamp = %s AND ExamType = %s AND ScannedAt = %s;"
        exam_attempt_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                (self.expected_exam_id, self.expected_student_matriculation_number_1,
                                                                 self.expected_room_name, self.expected_score_1,
                                                                 self.expected_grade_1, self.expected_written_in_semester,
                                                                 self.expected_duration_in_minutes, self.expected_start_time_stamp,
                                                                 self.expected_end_time_stamp, self.expected_exam_type,
                                                                 self.expected_scanned_at))
        if not exam_attempt_in_db:
            return LevelValidationResult(level="8.2",
                                         is_valid=False,
                                         message=f"Exam Attempt for student \"{self.expected_student_matriculation_number_1}\" does not exist in the Table \"ExamAttempt\".")
        statement: str = "SELECT * FROM ExamAttempt WHERE ExamId = %s AND StudentMatriculationnumber = %s AND RoomName = %s AND Score = %s AND Grade = %s AND WrittenInSemester = %s AND DurationInMinutes = %s AND StartTimeStamp = %s AND EndTimeStamp = %s AND ExamType = %s AND ScannedAt = %s;"
        exam_attempt_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                     (self.expected_exam_id, self.expected_student_matriculation_number_2,
                                                                      self.expected_room_name, self.expected_score_2,
                                                                      self.expected_grade_2, self.expected_written_in_semester,
                                                                      self.expected_duration_in_minutes, self.expected_start_time_stamp,
                                                                      self.expected_end_time_stamp, self.expected_exam_type,
                                                                      self.expected_scanned_at))
        if not exam_attempt_in_db:
            return LevelValidationResult(level="8.2",
                                         is_valid=False,
                                         message=f"Exam Attempt for student \"{self.expected_student_matriculation_number_2}\" does not exist in the Table \"ExamAttempt\".")
        statement: str = "SELECT * FROM ExamAttempt WHERE ExamId = %s AND StudentMatriculationnumber = %s AND RoomName = %s AND Score = %s AND Grade = %s AND WrittenInSemester = %s AND DurationInMinutes = %s AND StartTimeStamp = %s AND EndTimeStamp = %s AND ExamType = %s AND ScannedAt = %s;"
        exam_attempt_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                     (self.expected_exam_id, self.expected_student_matriculation_number_3,
                                                                      self.expected_room_name, self.expected_score_3,
                                                                      self.expected_grade_3, self.expected_written_in_semester,
                                                                      self.expected_duration_in_minutes, self.expected_start_time_stamp,
                                                                      self.expected_end_time_stamp, self.expected_exam_type,
                                                                      self.expected_scanned_at))
        if not exam_attempt_in_db:
            return LevelValidationResult(level="8.2",
                                         is_valid=False,
                                         message=f"Exam Attempt for student \"{self.expected_student_matriculation_number_3}\" does not exist in the Table \"ExamAttempt\".")
        return LevelValidationResult(level="8.2",
                                     is_valid=True,
                                     message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 8 and task_number == 2
