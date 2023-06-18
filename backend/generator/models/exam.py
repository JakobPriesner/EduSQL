from dataclasses import dataclass
from typing import Optional


@dataclass
class Exam:
    lecture_id: int
    allowed_attempts: int
    id: Optional[int] = None
