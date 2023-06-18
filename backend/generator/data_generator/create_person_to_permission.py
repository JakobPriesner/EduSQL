
# create an async function or class with async function that creates a person_to_permission.

import asyncio
import random
from dataclasses import fields

from generator.database.db_handler import DbHandler
from generator.models.person_to_permission import PersonToPermission


class GeneratePersonToPermission:
    def __init__(self) -> None:
        pass

    async def generate_all_person_to_permissions(self) -> None:
        person_to_permissions: list[PersonToPermission] = await self.__get_new_person_to_permissions()
        await self.store_person_to_permissions(person_to_permissions)

    async def __get_new_person_to_permissions(self) -> list[PersonToPermission]:
        return [
            await self.__new_person_to_permission()
            for x in range(500)
        ]

    async def __new_person_to_permission(self) -> PersonToPermission:

        int_array_person_id = await GeneratePersonToPermission.generate_persons()
        int_array_permission_id = await GeneratePersonToPermission.generate_permissions()

        return PersonToPermission(
            person_id=random.choice(int_array_person_id),
            permission_id=random.choice(int_array_permission_id),
        )

    @staticmethod
    async def generate_persons() -> list[int]:
        rows = await DbHandler.query_all("SELECT id from person;")
        return [_id for _id, in rows]

    @staticmethod
    async def generate_permissions() -> list[int]:
        rows = await DbHandler.query_all("SELECT id from permission")
        return [_id for _id, in rows]

    async def store_person_to_permissions(self, person_to_permissions: list[PersonToPermission]) -> None:
        person_to_permissions = list(set(person_to_permissions))
        sql: str = f"""
                    INSERT INTO persontopermission
                    (personid, permissionid)
                    VALUES {', '.join('(%s, %s)' for _ in person_to_permissions)};
                    """
        await DbHandler.execute(sql, *[item for item in tuple(getattr(entry, field.name) for entry in person_to_permissions
                                                                    for field in fields(entry) if field.name != "id")])


async def create_person_to_permissions() -> None:
    generator: GeneratePersonToPermission = GeneratePersonToPermission()
    await generator.generate_all_person_to_permissions()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_person_to_permissions())
