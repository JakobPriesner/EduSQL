import asyncio
import os
from typing import Optional

from injector import inject
from retrying import retry

from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection

import aiopg

from log.logger_interface import ILogger


class PostgresqlConnection(IPostgresqlConnection):
    @staticmethod
    def get_connection_string(user: DbUser, db_name: str) -> str:
        return f"postgresql://{user.username}:{user.password}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{db_name}"

    @inject
    def __init__(self, logger: ILogger):
        self._connection_string = os.getenv("PG_URL")
        self._logger = logger

    @retry(stop_max_attempt_number=4, wait_fixed=500)
    async def execute_without_response(self, user, db, sql: str, args: Optional[tuple] = None) -> None:
        self._logger.info(f"Executing SQL statement: {sql} with args {args}")
        async with await aiopg.connect(self.get_connection_string(user, db)) as conn:
            async with await conn.cursor() as cur:
                await cur.execute(sql, args)

    @retry(stop_max_attempt_number=4, wait_fixed=500)
    async def _execute_sql(self, user, db, sql: str, args: Optional[tuple] = None) -> int:
        self._logger.info(f"Executing SQL statement: {sql} with args {args}")
        async with await aiopg.connect(self.get_connection_string(user, db)) as conn:
            async with await conn.cursor() as cur:
                await cur.execute(sql, args)
                return cur.lastrowid

    @retry(stop_max_attempt_number=4, wait_fixed=500)
    async def execute_query(self, user, db, sql: str, args: Optional[tuple] = None) -> list[dict]:
        self._logger.info(f"Executing SQL statement: {sql} with args {args}")
        async with await aiopg.connect(self.get_connection_string(user, db)) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args)
                result = await cur.fetchall()
                return [dict(row) for row in result]

    @retry(stop_max_attempt_number=4, wait_fixed=500)
    async def _execute_query_single(self, user, db, sql: str, args: Optional[tuple] = None) -> Optional[dict]:
        self._logger.info(f"Executing SQL statement: {sql} with args {args}")
        async with await aiopg.connect(self.get_connection_string(user, db)) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args)
                return await cur.fetchone()

    async def create_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> int:
        return await self._execute_sql(user, db, sql, args)

    async def create_many_by_sql(self, user: DbUser, db: str, sql: str, args: list[tuple]) -> list[int]:
        result = await asyncio.gather(
            *[self._execute_sql(user, db, sql, entry) for entry in args]
        )
        return []  # todo

    async def load_all_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> list[dict]:
        return await self.execute_query(user, db, sql, args)

    async def load_single_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> Optional[dict]:
        return await self._execute_query_single(user, db, sql, args)

    async def update_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> int:
        return await self._execute_sql(user, db, sql, args)

    async def delete_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> int:
        return await self._execute_sql(user, db, sql, args)

    async def create_database(self, user: DbUser, db: str, new_db_name: str) -> None:
        sql: str = f"""
            CREATE DATABASE "{new_db_name}" 
                WITH TEMPLATE template 
                OWNER admin 
                ENCODING 'UTF8' 
                CONNECTION LIMIT = -1;
        """
        self._logger.info(f"Executing SQL statement: {sql}")
        async with await aiopg.connect(self.get_connection_string(user, db)) as conn:
            async with await conn.cursor() as cur:
                await cur.execute(sql)

    @staticmethod
    def result_to_dict(result, cursor) -> dict[str, any]:
        column_names = [column.name for column in cursor.description]
        return {column_name: value for column_name, value in zip(column_names, result)}
