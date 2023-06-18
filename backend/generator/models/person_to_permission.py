from dataclasses import dataclass


@dataclass
class PersonToPermission:
    person_id: int
    permission_id: int

    def __hash__(self):
        return hash((self.person_id, self.permission_id))