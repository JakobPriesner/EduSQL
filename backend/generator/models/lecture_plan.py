from dataclasses import dataclass
from datetime import date, time
from typing import Optional

from generator.models.enums.lecture_type_enum import LectureType


@dataclass
class LecturePlan:
    semester_specific_lecture_id: int
    staff_id: int
    room_name: str
    date: date
    start: time
    end: time
    type: LectureType
    notes: str
    id: Optional[int] = None
