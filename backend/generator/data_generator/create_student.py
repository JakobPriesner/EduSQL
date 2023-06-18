
# create an async function or class with async function that creates a student.

import asyncio
import platform
import random
from dataclasses import fields
from datetime import datetime
from typing import Optional

from generator.data.csv_loader import load_csv_file_as_generator
from generator.data_generator.create_degree import CreateDegree
from generator.data_generator.create_person import GeneratePerson
from generator.database.db_handler import DbHandler
from generator.models.student import Student


class GenerateStudent:

    def __init__(self):
        self.generate_person = GeneratePerson()
        self.generate_degree = CreateDegree()

    async def __async_init__(self):
        self.person_ids = await self.get_all_person_ids()
        self.degree_ids = await self.get_all_degree_ids()

    async def generate_all_students(self) -> None:
        students: list[Student] = await self.__get_new_students()
        await self.store_student(students)

    async def __get_new_students(self) -> list[Student]:
        return [
            self.__csv_to_student(*row)
            for row in load_csv_file_as_generator("student.csv")
        ]

    def __csv_to_student(self, matriculation_number, etc_score, in_student_council, enrolled_at, exmatriculated_at) -> Student:
        if self.person_ids:
            person_id: int = random.choice(self.person_ids)
            self.person_ids.remove(person_id)
        else:
            person_id: int = -1
        enrolled_at_as_list: list[str] = enrolled_at.split(".")
        exmatriculated_at_as_list: list[str] = exmatriculated_at.split(".")
        exmatriculated_at_obj: Optional[datetime] = datetime(year=int(exmatriculated_at_as_list[2]), month=int(exmatriculated_at_as_list[1]), day=int(exmatriculated_at_as_list[0]), hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59)) if exmatriculated_at else None
        return Student(
            matriculation_number=matriculation_number,
            person_id=person_id,
            degree_id=random.choice(self.degree_ids),
            etc_score=etc_score,
            in_student_council=in_student_council,
            enrolled_at=datetime(year=int(enrolled_at_as_list[2]), month=int(enrolled_at_as_list[1]), day=int(enrolled_at_as_list[0]), hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59)),
            exmatriculated_at=exmatriculated_at_obj,
        )

    @staticmethod
    async def get_all_person_ids() -> list:
        rows = await DbHandler.query_all("SELECT id from person")
        return [_id for _id, in rows]

    @staticmethod
    async def get_all_degree_ids() -> list:
        rows = await DbHandler.query_all("SELECT id from degree")
        return [_id for _id, in rows]

    async def store_student(self, student: list[Student]) -> None:
        sql: str = f"""
                    INSERT INTO student
                    (MatriculationNumber, PersonId, DegreeId, EtcsScore, InStudentCouncil, EnrolledAt, ExmatriculatedAt)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s, %s)' for _ in student)};
                    """
        await DbHandler.execute(sql, *[item if type(item) is not datetime else item.isoformat() for item in tuple(getattr(entry, field.name) for entry in student
                                                                    for field in fields(entry) if field.name != "id")])


async def create_students() -> None:
    generator: GenerateStudent = GenerateStudent()
    await generator.__async_init__()
    await generator.generate_all_students()


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_students())
