from enum import Enum


class ExamType(str, Enum):
    Written = "Written",
    Colloquium = "Colloquium",
    EvaExam = "EvaExam",
    Presentation = "Presentation",
    Portfolio = "Portfolio"
