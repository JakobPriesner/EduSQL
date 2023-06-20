import asyncio
import traceback

import aiopg
from aiopg import Pool

from generator.database.connection_string import get_connection_string


class DbHandler:
    __pool: Pool = None
    __waiting_tasks = 0

    @classmethod
    async def __async_init__(cls):
        cls.__pool = await aiopg.create_pool(get_connection_string(), minsize=10, maxsize=90)

    @classmethod
    async def get_pool(cls):
        incremented: bool = False
        if cls.__pool.freesize == 0:
            cls.__waiting_tasks += 1
            incremented = True
        while cls.__pool.freesize == 0:
            await asyncio.sleep(0.25)
        if incremented:
            cls.__waiting_tasks -= 1
        return cls.__pool

    @classmethod
    async def execute(cls, query, *args):
        pool = await cls.get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(query, args)
                    return cursor.lastrowid;
                except Exception as e:
                    pass

    @classmethod
    async def query(cls, query, *args):
        pool = await cls.get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchone()

    @classmethod
    async def query_all(cls, query, *args):
        pool = await cls.get_pool()
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    try:
                        await cursor.execute(query, args)
                        return await cursor.fetchall()
                    except Exception as e:
                        return []
        except Exception as e:
            traceback.print_exc()
            await cls.query_all(query, args)

    @classmethod
    async def close(cls):
        print("Closing DB connection pool")
        if cls.__pool is not None:
            while cls.__waiting_tasks > 0:
                print(f"Still waiting for tasks to finish: {cls.__waiting_tasks}")
                await asyncio.sleep(0.25)
            await asyncio.sleep(1)
            cls.__pool.close()
            await cls.__pool.wait_closed()
