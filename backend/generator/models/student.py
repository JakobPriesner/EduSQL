from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Student:
    matriculation_number: int
    person_id: int
    degree_id: int
    etc_score: float
    in_student_council: bool
    enrolled_at: datetime
    exmatriculated_at: Optional[datetime]
