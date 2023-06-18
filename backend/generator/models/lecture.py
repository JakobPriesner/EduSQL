from dataclasses import dataclass
from typing import Optional

from generator.models.enums.lecture_type_enum import LectureType


@dataclass
class Lecture:
    name: str
    description: str
    modulenumber: str
    required_etcs: int
    earned_etcs: int
    semester: int
    type: LectureType
    id: Optional[int] = None
