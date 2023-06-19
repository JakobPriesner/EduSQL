
# create an async function or class with async function that creates a person.

import asyncio
import random
from dataclasses import fields
from datetime import date

import psycopg

from generator.data.csv_loader import load_csv_file_as_generator
from generator.data_generator.create_address import GenerateAddress
from generator.database.db_handler import DbHandler
from generator.database.connection_string import get_connection_string
from generator.models.person import Person


class GeneratePerson:

    def __init__(self):
        self.generate_address = GenerateAddress()

    async def generate_all_persons(self) -> None:
        persons: list[Person] = await self.__get_new_persons()
        await self.store_persons(persons)

    async def __get_new_persons(self) -> list[Person]:
        tasks = [self.__csv_to_person(*row) for row in load_csv_file_as_generator("person.csv")]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [result for result in results if not isinstance(result, BaseException)]

    @staticmethod
    async def __csv_to_person(first_name, last_name, title_id, date_of_birth, email, k_number, password_hash, salt,
                                            session_token) -> Person:
        int_array = await GeneratePerson.generate_addresses()
        date_as_list: list[str] = date_of_birth.split(".")

        return Person(
            address_id=random.choice(int_array),
            first_name=first_name,
            last_name=last_name,
            title_id=title_id,
            date_of_birth=date(year=int(date_as_list[2]), month=int(date_as_list[1]), day=int(date_as_list[0])),
            email=email,
            k_number=k_number,
            password_hash=password_hash,
            salt=salt[:49],
            session_token=session_token,
        )

    @staticmethod
    async def generate_addresses() -> list[int]:
        # Man muss die address ID holen und dann einfügen
        rows = await DbHandler.query_all("SELECT id from address;")
        return [_id for _id, in rows]

    async def store_persons(self, persons: list[Person]) -> None:
        sql: str = f"""
                    INSERT INTO person
                    (addressid, firstname, lastname, titleid, dateofbirth, email, knumber, passwordhash, salt, sessiontoken)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' for _ in persons)};
                    """
        await DbHandler.execute(sql, *[item for item in tuple(getattr(entry, field.name) for entry in persons
                                                                    for field in fields(entry) if field.name != "id")])


async def create_persons() -> None:
    generator: GeneratePerson = GeneratePerson()
    await generator.generate_all_persons()


if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_persons())
