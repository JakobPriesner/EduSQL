from dataclasses import dataclass
from typing import Optional


@dataclass
class BusinessHours:
    monday_id: int
    tuesday_id: int
    wednesday_id: int
    thursday_id: int
    friday_id: int
    saturday_id: int
    sunday_id: int
    feast_day_id: int
    id: Optional[int] = None
