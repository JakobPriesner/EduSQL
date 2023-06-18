from dataclasses import dataclass
from typing import Optional


@dataclass
class Restriction:
    name: str
    description: str
    id: Optional[int] = None
