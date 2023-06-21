# create an async function or class with async function that creates a address.

from dataclasses import fields

from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.db_handler import DbHandler
from generator.models.address import Address


class GenerateAddress:
    def __init__(self) -> None:
        pass

    async def generate_all_addresses(self) -> None:
        await self.store_address_from_scv(self.__get_new_addresses())

    def __get_new_addresses(self) -> list[Address]:
        return [self.__csv_to_address(*row) for row in load_csv_file_as_generator("address.csv")]

    @staticmethod
    def __csv_to_address(street, house_number, address_addition, city, country, postal_code) -> Address:
        return Address(
            street=street,
            house_number=house_number,
            address_addition=address_addition,
            city=city,
            country=country,
            postal_code=postal_code,
        )

    async def store_address(self, address: Address) -> int:
        sql: str = f""" 
                    INSERT INTO address
                    (street, housenumber, addressaddition, city, country, postalcode)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """
        id, = await DbHandler.query(sql, address.street, address.house_number, address.address_addition, address.city,
                                     address.country, address.postal_code)
        return id

    async def store_address_from_scv(self, addresses: list[Address]) -> None:
        sql: str = f""" 
                    INSERT INTO address
                    (street, housenumber, addressaddition, city, country, postalcode)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s)' for _ in addresses)};
                    """
        await DbHandler.execute(sql, *[item for item in tuple(getattr(entry, field.name) for entry in addresses
                                                                   for field in fields(entry) if field.name != "id")])


async def create_addresses() -> None:
    generator: GenerateAddress = GenerateAddress()
    await generator.generate_all_addresses()
