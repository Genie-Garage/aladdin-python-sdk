from aiohttp import ClientSession, ClientResponse
import logging

from .model import GarageDoor
from .auth import Auth


class AladdinConnectClient:
    """Aladdin Connect API Client"""

    def __init__(self, session: Auth):
        self._session = session
        self._logger = logging.getLogger(__name__)
        self._doors = []

    async def get_doors(self) -> list[GarageDoor]:
        response = await self._session.request("GET", "devices")
        data = await response.json()

        doors = []
        for device in data["devices"]:
            for door in device["doors"]:
                doors.append(GarageDoor({
                    "device_id": device["id"],
                    "door_number": door["index"],
                    "name": door["name"],
                    "status": door["status"],
                    "link_status": door["link_status"],
                    "battery_level": door.get("battery", 0),
                }))

        self._logger.debug(f"ALADDIN GET DOORS RESULT: {doors}")
        self._doors = doors
        return doors

    async def update_door(self, device_id: str, door_number: int):
        current: GarageDoor | None = None
        for door in self._doors:
            if door.device_id == device_id and door.door_number == door_number:
                current = door
                break

        if current == None:
            self._logger.warn(f"Attempted to update non-existant door {device_id}-{door_number}")
            return

        response = await self._session.request("GET", f"devices/{device_id}/doors/{door_number}")
        data = await response.json()
        current.status = data["status"]
        current.link_status = data["linkStatus"]
        current.battery_level = data.get("battery_level", 0)

        self._logger.debug(f"ALADDIN UPDATE DOOR RESULT: {current}")
        self._doors = [current if d.unique_id == current.unique_id else d for d in self._doors]

    async def open_door(self, device_id: str, door_index: int) -> bool:
        return await self._issue_command(device_id, door_index, "open")

    async def close_door(self, device_id: str, door_index: int) -> bool:
        return await self._issue_command(device_id, door_index, "close")

    def get_door_status(self, device_id, door_number):
        """Get the door status."""
        for door in self._doors:
            if door.device_id == device_id and door.door_number == door_number:
                return door.status

    def get_battery_status(self, device_id, door_number):
        """Async call to get battery status for door."""
        for door in self._doors:
            if door.device_id == device_id and door.door_number == door_number:
                return door.battery_level
        return None

    async def _issue_command(self, device_id: str, door_index: int, command: str) -> bool:
        self._logger.debug(f"SENDING COMMAND {command} TO {device_id}_{door_index}")
        resp = await self._session.request(
            "POST", f"devices/{device_id}/doors/{door_index}/command",
            json={"command": command}
        )
        self._logger.debug(f"RESPONSE: {resp}")
        if resp.status > 299:
            return False
        return True
