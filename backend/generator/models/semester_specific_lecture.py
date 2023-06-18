from dataclasses import dataclass

from generator.models.enums.exam_type_enum import ExamType


@dataclass
class SemesterSpecificLecture:
    lecture_id: int
    semester_date: str
    student_count: int
    exam_type: ExamType
