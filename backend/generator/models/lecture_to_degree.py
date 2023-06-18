from dataclasses import dataclass


@dataclass
class LectureToDegree:
    degree_id: int
    lecture_id: int

    def __hash__(self):
        return hash((self.degree_id, self.lecture_id))
