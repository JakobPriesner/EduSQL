import asyncio
from dataclasses import fields

from generator.database.db_handler import DbHandler
from generator.models.enums.lecture_type_enum import LectureType
from generator.models.exam import Exam
from generator.models.lecture import Lecture


class CreateExam:

    async def __init_async__(self) -> None:
        self.lectures: list[Lecture] = await self.__load_all_lectures_async()

    async def generate_all_exams(self) -> None:
        exams: list[Exam] = [self.__generate_new_exam(lecture) for lecture in self.lectures]
        await self.__store_all_exams_async(exams)

    def __generate_new_exam(self, lecture: Lecture) -> Exam:
        if lecture.type == LectureType.Awpf:
            exam: Exam = Exam(lecture_id=lecture.id, allowed_attempts=2147483647)   # sys.maxsize ist größer als INT
        else:
            exam: Exam = Exam(lecture_id=lecture.id, allowed_attempts=3)
        return exam

    @staticmethod
    async def __store_all_exams_async(exam_to_store: list[Exam]) -> None:
        sql: str = f"""
                    INSERT INTO exam
                    (lectureid, allowedattempts)
                    VALUES {', '.join('(%s, %s)' for _ in exam_to_store)};
                    """
        await DbHandler.execute(sql, *[item for item in tuple(
                    getattr(entry, field.name) for entry in exam_to_store for field in fields(entry) if
                    field.name != "id")])

    @staticmethod
    async def __load_all_lectures_async() -> list[Lecture]:
        sql: str = "SELECT * from lecture"
        results: list[tuple] = await DbHandler.query_all(sql)
        return [
            Lecture(name, description, modulenumber, required_etcs, earned_etcs, semester, type, id)
            for id, name, description, modulenumber, required_etcs, earned_etcs, semester, type in results
        ]


async def create_exams() -> None:
    exams = CreateExam()
    await exams.__init_async__()
    await exams.generate_all_exams()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_exams())
