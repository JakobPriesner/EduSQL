from dataclasses import dataclass
from typing import Optional


@dataclass
class Permission:
    alias: str
    description: str
    id: Optional[int] = None
