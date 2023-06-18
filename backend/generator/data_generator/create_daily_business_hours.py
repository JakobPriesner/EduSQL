import asyncio
from datetime import time

from generator.database.db_handler import DbHandler
from generator.models.daily_business_hours import DailyBusinessHours


class GenerateDailyBusinessHours:
    async def store_daily_business_hours(self, dailybusinesshours: DailyBusinessHours) -> int:

        sql: str = f""" 
                    INSERT INTO dailyBusinessHours
                    (starttime, endtime)
                    VALUES (%s, %s)
                    RETURNING id;
                    """
        return await DbHandler.query(sql, dailybusinesshours.start, dailybusinesshours.end)


async def create_daily_business_hours() -> None:
    new_morning = DailyBusinessHours(start=time(hour=8, minute=30), end=time(hour=12))
    new_afternoon = DailyBusinessHours(start=time(hour=12), end=time(hour=16))
    new_daily = DailyBusinessHours(start=time(hour=8, minute=30), end=time(hour=14))
    new_close = DailyBusinessHours(start=time(hour=0), end=time(hour=0))

    generator: GenerateDailyBusinessHours = GenerateDailyBusinessHours()
    await asyncio.gather(
        generator.store_daily_business_hours(new_morning),
        generator.store_daily_business_hours(new_afternoon),
        generator.store_daily_business_hours(new_daily),
        generator.store_daily_business_hours(new_close)
    )

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_daily_business_hours())
