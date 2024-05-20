import asyncio
import random
from dataclasses import fields
from datetime import date

from generator.data.csv_loader import load_csv_file_as_generator
from generator.data_generator.create_person import GeneratePerson
from generator.database.db_handler import DbHandler
from generator.models.staff import Staff


class GenerateStaff:

    def __init__(self):
        self.generate_person = GeneratePerson()
        self.person_ids = None
        # self.generate_room = GenerateRoom()

    async def generate_all_staffs(self) -> None:
        self.person_ids = await self.get_all_person_ids()
        staffs: list[Staff] = await self.__get_new_staffs()
        await self.store_staff(staffs)

    async def __get_new_staffs(self) -> list[Staff]:
        return [self.__csv_to_staff(*row) for row in load_csv_file_as_generator("staff.csv")]

    def __csv_to_staff(self, staff_type, salary, temporary_to, employed_since, hours_per_week, holidays, social_security_id, iban, released, paused) -> Staff:
        temporary_to_as_list: list[str] = temporary_to.split(".")
        employed_since_as_list: list[str] = employed_since.split(".")
        released_as_list = released.split(".")
        paused_as_list = paused.split(".")

        return Staff(
            person_id=random.choice(self.person_ids),
            reports_to_id=random.choice(self.person_ids),
            room_name="", # todo
            staff_type=staff_type,
            salary=salary,
            temporary_to=date(year=int(temporary_to_as_list[2]), month=int(temporary_to_as_list[1]), day=int(temporary_to_as_list[0])),
            employed_since=date(year=int(employed_since_as_list[2]), month=int(employed_since_as_list[1]), day=int(employed_since_as_list[0])),
            hours_per_week=hours_per_week,
            holidays=holidays,
            social_security_id=social_security_id,
            iban=iban,
            released=date(year=int(released_as_list[2]), month=int(released_as_list[1]), day=int(released_as_list[0])) if released else None,
            paused=date(year=int(paused_as_list[2]), month=int(paused_as_list[1]), day=int(paused_as_list[0])) if paused else None,
        )

    @staticmethod
    async def get_all_person_ids() -> list[int]:
        rows = await DbHandler.query_all("SELECT id from person")
        return [_id for _id, in rows]

    async def store_staff(self, staffs: list[Staff]) -> None:
        sql: str = f"""
                    INSERT INTO staff
                    (personid, reportstoid, roomname, stafftype, salary, temporaryto, employedsince, hoursperweek, holidays, socialsecurityid, iban, released, paused)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' for _ in staffs)};
                    """
        await DbHandler.execute(sql, *[item if type(date) else item.isoformat() for item in tuple(getattr(entry, field.name) for entry in staffs
                                                                    for field in fields(entry) if field.name != "id")])


async def create_staffs() -> None:
    generator: GenerateStaff = GenerateStaff()
    await generator.generate_all_staffs()
