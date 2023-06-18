import asyncio
import random
import time
from typing import Optional

from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler


class LectureGenerator:
    def __init__(self):
        self.room_dict = {Modulenumber: room for _, _, _, _, _, _, room, _, _, _, Modulenumber in load_csv_file_as_generator("vl_plan.csv")}
        self.module_number_to_lecture_id = {}

    async def create_sslecture(self):
        await self.load_lecture_ids()
        lectures = await asyncio.gather(*[self.process_row(modulenumbers, SemesterDate, typeofexam, LectureType) for
                               _, _, _, _, _, _, _, _, _, _, _, _, _, _, modulenumbers, LectureType, _, _, _, _, _, _, _, typeofexam, SemesterDate, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _
                               in load_csv_file_as_generator("moduledescription.csv")])
        sql = "INSERT INTO semesterspecificlecture (LectureId, SemesterDate, RoomName, StudentCount, ExamType, LectureType) VALUES (%s, %s, %s, %s, %s, %s);"
        await asyncio.gather(*[DbHandler.execute(sql, *sublist) for sublist in lectures if sublist])

    async def process_row(self, module_numbers, semester_date, type_of_exam, lecture_type) -> Optional[tuple]:
        room_name = self.get_roomname(module_numbers)
        lecture_id = self.module_number_to_lecture_id.get(module_numbers.replace(" ", "").split(",")[0], -1)
        if not lecture_id:
            print(f"Could not find the lectureId of module_numbers: {module_numbers}")
            return None
        student_count = random.randint(10, 120)
        return lecture_id, semester_date, room_name, student_count, type_of_exam, lecture_type

    def get_roomname(self, modulenumber):
        return self.room_dict.get(modulenumber, "H.1.1")

    async def load_lecture_ids(self):
        sql = "SELECT id, modulenumber FROM lecture;"
        result = await DbHandler.query_all(sql)
        self.module_number_to_lecture_id = {modulenumber: id for id, modulenumber in result}


async def create_sslecture():
    generator = LectureGenerator()
    await generator.create_sslecture()


if __name__ == '__main__':
    asyncio.run(create_sslecture())
