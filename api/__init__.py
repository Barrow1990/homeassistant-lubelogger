from __future__ import annotations

from .vehicles import VehicleApi
from .odometer import OdometerApi
from .service_records import ServiceRecordApi
from .fuel import FuelApi


class LubeLoggerApi:
    """Unified API wrapper for all LubeLogger endpoints."""

    def __init__(self, base_url: str, username: str, password: str):
        self.vehicles = VehicleApi(base_url, username, password)
        self.odometer = OdometerApi(base_url, username, password)
        self.service_records = ServiceRecordApi(base_url, username, password)
        self.fuel = FuelApi(base_url, username, password)
