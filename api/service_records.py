from __future__ import annotations
from .base import LubeLoggerApiBase


class ServiceRecordApi(LubeLoggerApiBase):

    async def list(self, vehicle_id: int):
        return await self._request(
            "GET",
            f"/api/vehicle/servicerecords/list?vehicleId={vehicle_id}"
        )

    async def add(self, vehicle_id: int, data: dict):
        return await self._request(
            "POST",
            f"/api/vehicle/servicerecords/add?vehicleId={vehicle_id}",
            json=data,
        )
