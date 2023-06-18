from dataclasses import dataclass


@dataclass(frozen=True)
class DbUser:
    username: str
    password: str
