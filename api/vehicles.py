from __future__ import annotations
from .base import LubeLoggerApiBase


class VehicleApi(LubeLoggerApiBase):

    async def vehicles_list(self):
        return await self._request("GET", "/api/vehicles")

    async def get(self, vehicle_id: int):
        return await self._request("GET", f"/api/vehicle/get?id={vehicle_id}")
