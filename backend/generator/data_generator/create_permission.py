
# create an async function or class with async function that creates a permission.

import asyncio
from dataclasses import fields

from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler
from generator.models.permission import Permission


class GeneratePermission:
    def __init__(self) -> None:
        pass

    async def generate_all_permissions(self) -> None:
        permissions: list[Permission] = await self.__get_new_permissions()
        await self.store_permission(permissions)

    async def __get_new_permissions(self) -> list[Permission]:
        return [
            self.__csv_to_permission(*row)
            for row in load_csv_file_as_generator("permission.csv")
        ]

    def __csv_to_permission(self, alias, description) -> Permission:
        return Permission(
            alias=alias,
            description=description,
        )

    async def store_permission(self, permissions: list[Permission]) -> None:
        sql: str = f""" 
                    INSERT INTO permission
                    (alias, description)
                    VALUES {', '.join('(%s, %s)' for _ in permissions)};
                    """
        await DbHandler.execute(sql, *[item for item in tuple(getattr(entry, field.name) for entry in permissions
                                                              for field in fields(entry) if field.name != "id")])


async def create_permissions() -> None:
    generator: GeneratePermission = GeneratePermission()
    await generator.generate_all_permissions()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_permissions())
