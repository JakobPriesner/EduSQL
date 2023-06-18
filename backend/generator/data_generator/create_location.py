import asyncio
import random
from dataclasses import fields
from datetime import time


from generator.data.csv_loader import load_csv_file_as_generator
from generator.data_generator.create_address import GenerateAddress
from generator.data_generator.create_business_hours import GenerateBusinessHours
from generator.database.db_handler import DbHandler
from generator.models.address import Address
from generator.models.business_hours import BusinessHours
from generator.models.location import Location


class GenerateLocation:

    def __init__(self):
        self.generate_address = GenerateAddress()
        self.generate_business_hours = GenerateBusinessHours()

    async def generate_all_locations(self) -> None:
        locations: list[Location] = await self.__get_new_locations()
        await self.store_location(locations)

    async def __get_new_locations(self) -> list[Location]:
        return [
            await self.__csv_to_location(*row)
            for row in load_csv_file_as_generator("location.csv")
        ]

    async def __csv_to_location(self, area, lectureroomcount, building_count, mensa, parking_slots, library, street,
                                house_number,
                                address_addition, city, country, postal_code) -> Location:
        address_id: int = await self.generate_address.store_address(
            Address(street, house_number, address_addition, city, country, postal_code))

        int_array = await GenerateLocation.generate_business_hours()

        business_hours_id: int = await self.generate_business_hours.store_business_hours(
            BusinessHours(int_array[1], int_array[2], int_array[3], int_array[1], int_array[2], int_array[3],
                          int_array[0], int_array[0]))

        return Location(
            address_id=address_id,
            business_hours_id=business_hours_id,
            area=area,
            lectureroomcount=lectureroomcount,
            building_count=building_count,
            mensa=mensa,
            parking_slots=parking_slots,
            library=library,
        )

    @staticmethod
    async def generate_business_hours() -> list:
        int_array = []
        int_other_array = []
        int_random_array = []

        sql: str = "SELECT * from dailybusinesshours"
        rows = await DbHandler.query_all(sql)
        for row in rows:
            if row[1] == time(hour=0):
                int_array.append(row[0])
            else:
                int_other_array.append(row[0])

        for i in int_other_array:
            rand_index = random.randint(0, len(int_other_array) - 1)
            rand_int = int_other_array[rand_index]
            int_random_array.append(rand_int)

        int_array.extend(int_random_array)

        return int_array

    async def store_location(self, locations: list[Location]) -> int:
        sql: str = f""" 
                    INSERT INTO location
                    (addressid, businesshoursid, area, lectureroomcount, buildingcount, mensa, parkingslots, library)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s, %s, %s)' for _ in locations)}
                    RETURNING id;
                    """

        return await DbHandler.query(sql, *[item for item in tuple(getattr(entry, field.name) for entry in locations
                                                                   for field in fields(entry) if field.name != "id")])


async def create_locations() -> None:
    generator: GenerateLocation = GenerateLocation()
    await generator.generate_all_locations()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_locations())
