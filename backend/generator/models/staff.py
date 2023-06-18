from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class StaffType(str, Enum):
    Professor = "Professor",
    ExternalAssistant = "ExternalAssistant",
    ResearchAssistant = "ResearchAssistant",
    StudentAssistant = "StudentAssistant"


@dataclass
class Staff:
    person_id: int
    reports_to_id: int
    room_name: str
    staff_type: StaffType
    salary: float
    temporary_to: date
    employed_since: date
    hours_per_week: float
    holidays: float
    social_security_id: int
    iban: str
    released: Optional[date]
    paused: Optional[date]
    id: Optional[int] = None
