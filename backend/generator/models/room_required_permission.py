from dataclasses import dataclass


@dataclass
class RoomRequiredPermission:
    permission_id: int
    room_name: str
