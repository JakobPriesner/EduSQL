from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    address_id: int
    business_hours_id: int
    area: int
    lectureroomcount: int
    building_count: int
    mensa: bool
    parking_slots: int
    library: bool
    id: Optional[int] = None
    