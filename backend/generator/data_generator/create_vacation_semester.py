
# create an async function or class with async function that creates a vacation_semester.

import asyncio
import random
import time

from generator.data.csv_loader import load_csv_file_as_generator
from generator.data_generator.create_student import GenerateStudent
from generator.database.db_handler import DbHandler
from generator.models.vacation_semester import VacationSemester


class GenerateVacationSemester:

    def __init__(self):
        self.generate_student = GenerateStudent()
        self.student_mat_numbers = []

    async def generate_all_vacation_semesters(self) -> None:
        self.student_mat_numbers = await self.get_all_student_mat_numbers()
        vacation_semesters: list[VacationSemester] = await self.__get_new_vacation_semesters()
        await self.store_vacation_semester(vacation_semesters)

    async def __get_new_vacation_semesters(self) -> list[VacationSemester]:
        return [
            self.__csv_to_vacation_semester(*row)
            for row in load_csv_file_as_generator("vacation_semester.csv")
        ]

    def __csv_to_vacation_semester(self, justification, approved, semestercount) -> VacationSemester:
        return VacationSemester(
            student_matriculation_number=random.choice(self.student_mat_numbers),
            justification=justification,
            approved=approved,
            semester_count=semestercount,
        )

    @staticmethod
    async def get_all_student_mat_numbers() -> list[int]:
        rows = await DbHandler.query_all("SELECT matriculationnumber from student")
        return [_matriculationnumber for _matriculationnumber, in rows]

    async def store_vacation_semester(self, vacation_semesters: list[VacationSemester]) -> None:
        sql: str = f""" 
                    INSERT INTO vacationsemester
                    (studentmatriculationnumber, justification, approved, semestercount)
                    VALUES {', '.join('(%s, %s, %s, %s)' for _ in vacation_semesters)};
                    """
        await DbHandler.execute(sql, vacation_semesters[0].student_matriculation_number, vacation_semesters[0].justification, vacation_semesters[0].approved, vacation_semesters[0].semester_count)


async def create_vacation_semesters() -> None:
    generator: GenerateVacationSemester = GenerateVacationSemester()
    await generator.generate_all_vacation_semesters()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_vacation_semesters())
