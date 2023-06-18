from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Person:
    address_id: int
    first_name: str
    last_name: str
    title_id: str
    date_of_birth: date
    email: str
    k_number: str
    password_hash: str
    salt: str
    session_token: str
    id: Optional[int] = None
