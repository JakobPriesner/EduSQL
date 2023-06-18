from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class DailyBusinessHours:
    start: time
    end: time
    id: Optional[int] = None
    