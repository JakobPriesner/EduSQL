import asyncio
from dataclasses import fields

from aiocache import cached

from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler
from generator.models.degree import Degree


class CreateDegree:

    async def generate_all_degrees_async(self) -> None:
        degrees_to_store: list[Degree] = [
            await self.__csv_to_degrees_async(name, degree_type, street, house_number, city)
            for _, _, _, degree_type, name, _, city, street, house_number in load_csv_file_as_generator("sre.csv")
        ]
        await self.__store_all_degrees_async(degrees_to_store)

    @staticmethod
    async def __store_all_degrees_async(degrees_to_store: list[Degree]) -> None:
        sql: str = f"""
                    INSERT INTO degree
                    (Name, LocationId, TotalEtc, DegreeType, SemesterCount)
                    VALUES {', '.join('(%s, %s, %s, %s, %s)' for _ in degrees_to_store)};
                    """

        await DbHandler.execute(sql, *[item for item in tuple(getattr(entry, field.name) for entry in degrees_to_store for field in fields(entry) if field.name != "id")])

    async def __csv_to_degrees_async(self, name:  str, degree_type: str, street: str, house_number: str, city: str) -> Degree:
        if city == "Würzburg":
            city = "Wuerzburg"
        location_id: int = await self.__load_location_id(street, house_number, city)
        if degree_type.startswith("Bachelor"):
            return Degree(name, location_id, 120, degree_type, 7)
        elif degree_type.startswith("Master"):
            return Degree(name, location_id, 90, degree_type, 3)
        else:
            raise ValueError(f"Got invalid DegreeType: \"{degree_type}\"")

    @staticmethod
    @cached(ttl=10)
    async def __load_location_id(street: str, house_number: str, city: str) -> int:
        sql: str = f"""
                    SELECT l.id FROM address
                    LEFT JOIN location l on address.id = l.addressid
                    WHERE street = %s AND housenumber = %s AND city = %s;
                    """
        result = await DbHandler.query(sql, street, house_number, city)
        return result


async def create_degrees() -> None:
    degrees = CreateDegree()
    await degrees.generate_all_degrees_async()

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_degrees())
