from dataclasses import dataclass
from typing import Optional


@dataclass
class VacationSemester:
    student_matriculation_number: int
    justification: str
    approved: bool
    semester_count: int
    id: Optional[int] = None
