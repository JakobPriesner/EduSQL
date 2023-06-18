import asyncio
from functools import lru_cache

from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler


async def create_room():
    for row in load_csv_file_as_generator("room.csv"):
        await process_row(row)


async def process_row(row):
    _, totalnumberofseats, _, campus, _, _, _, _, _, roomname, _, _, _, description, _, _, _, _, _, _, _, _, _, _, _, _ = row
    locationid = get_locationid(campus)
    sql = "INSERT INTO Room (roomname, locationid, description, numberofseats) VALUES (%s, %s, %s, %s)"
    await DbHandler.execute(sql, roomname, locationid, description, totalnumberofseats)


@lru_cache(maxsize=128)
def get_locationid(campus):
    for _, _, _, campus_val, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ in load_csv_file_as_generator("room.csv"):
        if campus_val == "SHL 20":
            return 5
        elif campus_val == "JMU":
            return 2
        elif campus_val == "Campus I":
            return 3
        elif campus_val.endswith("8"):  # RöRi 8
            return 4
        elif campus_val.endswith("12"):  # Mü 12
            return 1
    return 1



if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_room())
