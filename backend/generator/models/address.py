from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    street: str
    house_number: str
    address_addition: str
    city: str
    country: str
    postal_code: int
    id: Optional[int] = None
