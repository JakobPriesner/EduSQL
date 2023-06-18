import asyncio

import aiofiles as aiofiles
from injector import inject

from command_interface import ICommand
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class CreateAllTablesForSchema(ICommand):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")

    async def handle(self, user_uuid: str) -> None:
        await asyncio.gather(await self._db.create_by_sql(self._admin_user, user_uuid, statement)
                             for statement in await self._get_sql_statements(user_uuid))

    @staticmethod
    async def _get_sql_statements(user_uuid: str) -> list[str]:
        with aiofiles.open("../sqls/create_tables_for_new_schema.sql", "r") as file:
            sql_statements: list[str] = file.read().split("\n")
            return [statement.replace("{user_uuid}", user_uuid) for statement in sql_statements]
