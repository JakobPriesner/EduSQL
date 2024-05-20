import asyncio
import time
import uuid
from collections import defaultdict
from dataclasses import fields
from aiocache import cached
from dotenv import load_dotenv

from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler
from generator.models.enums.lecture_type_enum import LectureType
from generator.models.lecture import Lecture
from generator.models.restriction import Restriction
from generator.processing.process_handler import ProcessHandler

class LectureGenerator:
    def __init__(self):
        self.lectures: list[Lecture] = []
        self.module_number_to_restrictions: dict[str, list[Restriction]] = defaultdict(list)

    async def generate_all_lectures_async(self) -> None:
        self.__load_all_data()
        await self.__store_into_db()

    def __load_all_data(self) -> None:
        self.lectures = self.create_lectures()

    def process_row(self, row):
        _, _, earned_ects, _, _, _, _, _, _, semester, name, restrictions, _, _, module_numbers, lecture_type, description, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = row
        lectures = []
        for module_number in module_numbers.replace(" ", "").split(","):
            for semester in semester.replace(" ", "").split(","):
                required_ects: int = self.__extract_restrictions(restrictions, module_number)
                intern_lecture_type: LectureType = self.__extract_lecture_type(lecture_type)
                lectures.append(Lecture(
                    name=name,
                    description=description,
                    modulenumber=module_number,
                    required_etcs=required_ects,
                    earned_etcs=int(earned_ects),
                    semester=int(semester) if semester else 1,
                    type=intern_lecture_type
                ))
        return lectures

    def create_lectures(self):
        rows = load_csv_file_as_generator("moduledescription.csv")
        lectures = []
        for result in ProcessHandler.map(self.process_row, rows):
            lectures.extend(result)
        return lectures

    def __extract_restrictions(self, restrictions: str, module_number: str) -> int:
        splittet_restrictions: list[str] = [r for r in restrictions.split("; ") for r1 in r.split(", ") if r1]
        required_ects: int = 0
        for restriction in splittet_restrictions:
            if "keine" in restriction.lower():
                return 0
            elif any(phrase in restriction for phrase in [" ECTS", " CP"]):
                restriction = restriction.replace("> ", "").replace(">", "")
                try:
                    required_ects = int(restriction.split(" ")[0])
                except (ValueError, TypeError):
                    required_ects = 0
            else:
                self.module_number_to_restrictions[module_number].append(
                    Restriction(name=uuid.uuid4().hex[:29], description=restriction))
        return required_ects

    def __extract_lecture_type(self, lecture_type: str) -> LectureType:
        lower_lecture_type: str = lecture_type.lower()
        if any(phrase.lower() == lower_lecture_type for phrase in ["Seminar", "sem. Unterricht"]):
            return LectureType.Su
        elif any(phrase.lower() == lower_lecture_type for phrase in ["Vorlesung"]):
            return LectureType.Vl
        elif any(phrase.lower() in lower_lecture_type for phrase in ["Projekt"]):
            return LectureType.P
        elif any(phrase.lower() in lower_lecture_type for phrase in ["Übung"]):
            return LectureType.E
        return LectureType.Su

    async def __store_into_db(self) -> None:
        await self.__store_all_lectures_into_db()
        await self.__generate_and_store_restrictions_to_lectures_in_db()

    async def __generate_and_store_restrictions_to_lectures_in_db(self) -> None:
        for module_number, restrictions in self.module_number_to_restrictions.items():
            await self.__store_for_single_module_number(module_number, restrictions)

    async def __store_for_single_module_number(self, module_number, restrictions):
        lecture_id: int = await self.__get_lecture_id_by_module_name(module_number)
        for restriction in restrictions:
            await self.__store_lecture_to_restriction_into_db(lecture_id, await self.__store_restriction_into_db(restriction))

    async def __store_restriction_into_db(self, restriction: Restriction) -> int:
        sql: str = f"""
                    INSERT INTO Restriction
                    (Name, Description)
                    VALUES (%s, %s)
                    RETURNING id;
                    """
        return await DbHandler.query(sql, restriction.name, restriction.description)

    async def __store_all_lectures_into_db(self) -> None:
        sql: str = f"""
                    INSERT INTO Lecture
                    (Name, Description, ModuleNumber, RequiredEtcs, EarnedEtcs, Semester, Type)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s, %s)' for _ in self.lectures)};
                    """
        await DbHandler.execute(sql, *[item for item in
                                       tuple(getattr(entry, field.name) if type(entry) is not LectureType else getattr(
                                           entry,
                                           field.name).value
                                             for entry in self.lectures for field in fields(entry) if
                                             field.name != "id")])

    async def __store_lecture_to_restriction_into_db(self, lecture_id: int, restriction_id: int) -> None:
        sql: str = f"""
                    INSERT INTO LectureToRestriction
                    (LectureId, RestrictionId)
                    VALUES (%s, %s);
                    """
        await DbHandler.execute(sql, lecture_id, restriction_id)

    @staticmethod
    @cached(ttl=5)
    async def __get_lecture_id_by_module_name(module_number: str) -> int:
        sql: str = f"""
                    SELECT id FROM Lecture
                    WHERE modulenumber = %s;
                    """
        return await DbHandler.query(sql, module_number)


async def create_lectures() -> None:
    generator: LectureGenerator = LectureGenerator()
    await generator.generate_all_lectures_async()
