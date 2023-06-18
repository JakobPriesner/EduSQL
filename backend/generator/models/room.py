from dataclasses import dataclass


@dataclass
class Room:
    room_name: str
    location_id: int
    description: str
    number_of_seats: int
