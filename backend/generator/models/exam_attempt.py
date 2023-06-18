from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from generator.models.enums.exam_type_enum import ExamType


@dataclass
class ExamAttempt:
    exam_id: int
    student_matriculation_number: int
    room_name: str
    score: float
    grade: float
    written_in_semester: str
    duration_in_minutes: int
    start_time_stamp: datetime
    end_time_stamp: datetime
    exam_type: ExamType
    scanned_at: datetime
    id: Optional[int] = None
