from dataclasses import dataclass
from typing import Optional


@dataclass
class Degree:
    name: str
    location_id: int
    total_etc: int
    degree_type: str
    semester_count: int
    id: Optional[int] = None
