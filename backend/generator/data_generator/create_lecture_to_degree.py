import asyncio
import platform
from dataclasses import fields
from typing import Optional


from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler
from generator.models.degree import Degree
from generator.models.lecture import Lecture
from generator.models.lecture_to_degree import LectureToDegree


class GenerateLectureToDegree:
    async def __init_async__(self):
        self.lectures: list[Lecture] = await self.__load_all_lectures_async()
        self.degrees: list[Degree] = await self.__load_all_degrees_async()

    async def __generate_all_lecture_to_degrees__(self):
        lecture_to_degrees_to_store: list[LectureToDegree] = [
            lecture_to_degree
            for _, bec, _, bin, _, _, _, _, _, _, _, _, mis, _, modulenumber, _, _, _, _, _, _, _, bwi, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, mai, _, _, bis, mdb, _, bdg, _, _
            in load_csv_file_as_generator("moduledescription.csv")
            for lecture_to_degree in self.__csv_to_lecture_to_degree_async(bool(bec), bool(bin), bool(mis), modulenumber, bool(bwi), bool(mai), bool(mdb))
        ]
        result = [entry for entry in lecture_to_degrees_to_store if entry]
        lecture_to_degrees_to_store = list(set(result))
        await self.__store_all_lecture_to_degrees_async(lecture_to_degrees_to_store)

    def __csv_to_lecture_to_degree_async(self, bec: bool, bin: bool, mis: bool, modulenumber: str, bwi: bool, mai: bool, mdb: bool) -> Optional[list[LectureToDegree]]:
        # lecture = next(lecture for lecture in self.lectures if lecture.modulenumber == modulenumber)
        result_list: list[LectureToDegree] = []
        for lecture in self.lectures:
            if lecture.modulenumber == modulenumber:
                if bin:
                    result_list.append(self.__create_lecture_to_degree_connection(lecture.id, "BIN"))
                if bec:
                    result_list.append(self.__create_lecture_to_degree_connection(lecture.id, "BEC"))
                if bwi:
                    result_list.append(self.__create_lecture_to_degree_connection(lecture.id, "BWI"))
                if mis:
                    result_list.append(self.__create_lecture_to_degree_connection(lecture.id, "MIS"))
                if mdb:
                    result_list.append(self.__create_lecture_to_degree_connection(lecture.id, "MDB"))
                if mai:
                    result_list.append(self.__create_lecture_to_degree_connection(lecture.id, "MAI"))
                break
        return result_list

    def __create_lecture_to_degree_connection(self, lecture_id: int, degree_name: str) -> LectureToDegree:
        for degree in self.degrees:
            if degree.name == degree_name:
                return LectureToDegree(degree.id, lecture_id)

    async def __load_all_lectures_async(self) -> list[Lecture]:
        sql: str = "SELECT * from lecture"
        results: list[tuple] = await DbHandler.query_all(sql)
        return [
            Lecture(name, description, modulenumber, required_etcs, earned_etcs, semester, type, id)
            for id, name, description, modulenumber, required_etcs, earned_etcs, semester, type in
            results
        ]

    async def __load_all_degrees_async(self) -> list[Degree]:
        sql: str = "SELECT * from degree"
        results: list[tuple] = await DbHandler.query_all(sql)
        return [
            Degree(name, location_id, total_etc, degree_type, semester_count, id)
            for id, name, location_id, total_etc, degree_type, semester_count in results
        ]

    async def __store_all_lecture_to_degrees_async(self, lecture_to_degrees_to_store: list[LectureToDegree]):
        if len(lecture_to_degrees_to_store) == 0:
            return
        sql: str = f"""
                    INSERT INTO lecturetodegree
                    (degreeid, lectureid)
                    VALUES {', '.join('(%s, %s)' for _ in lecture_to_degrees_to_store)};
                    """
        await DbHandler.execute(sql, *[item for item in tuple(
                    getattr(entry, field.name) for entry in lecture_to_degrees_to_store for field in fields(entry))])


async def create_lecture_to_degrees() -> None:
    degrees = GenerateLectureToDegree()
    await degrees.__init_async__()
    await degrees.__generate_all_lecture_to_degrees__()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_lecture_to_degrees())
