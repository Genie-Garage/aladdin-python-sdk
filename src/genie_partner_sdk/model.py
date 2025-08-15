"""Models for Aladdin connect cover platform."""

from typing import TypedDict


class GarageDoorData(TypedDict):
    """Aladdin door data"""

    device_id: str
    door_number: int
    name: str
    status: str
    link_status: str
    battery_level: int


class GarageDoor:
    """Aladdin Garage Door Entity"""

    def __init__(self, data: GarageDoorData) -> None:
        self.device_id: str = data["device_id"]
        self.door_number: int = data["door_number"]
        self.unique_id: str = f"{self.device_id}-{self.door_number}"
        self.name: str = data["name"]
        self.status: str = data["status"]
        self.link_status: str = data["link_status"]
        self.battery_level: int = data["battery_level"]
