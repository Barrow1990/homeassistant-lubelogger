from __future__ import annotations
from .base import LubeLoggerApiBase


class OdometerApi(LubeLoggerApiBase):

    async def get_latest_odometer(self, vehicle_id: int):
        return await self._request(
            "GET",
            f"/api/vehicle/odometerrecords/latest?vehicleId={vehicle_id}"
        )

    async def add(self, vehicle_id: int, value: float, date: str):
        return await self._request(
            "POST",
            f"/api/vehicle/odometerrecords/add?vehicleId={vehicle_id}",
            json={"odometer": value, "date": date},
        )
