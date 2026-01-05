from __future__ import annotations
from .base import LubeLoggerApiBase


class FuelApi(LubeLoggerApiBase):

    async def list(self, vehicle_id: int):
        return await self._request(
            "GET",
            f"/api/vehicle/fuelrecords/list?vehicleId={vehicle_id}"
        )

    async def add(self, vehicle_id: int, data: dict):
        return await self._request(
            "POST",
            f"/api/vehicle/fuelrecords/add?vehicleId={vehicle_id}",
            json=data,
        )
