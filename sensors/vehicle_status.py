from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry

from ..const import DOMAIN
from .utils import build_vehicle_name


class LubeLoggerVehicleStatusSensor(SensorEntity):
    """Main status sensor for a LubeLogger vehicle."""

    _attr_icon = "mdi:car-info"
    _attr_primary = False
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry, vehicle: dict[str, Any]):
        self._entry = entry
        self._vehicle = vehicle

        vehicle_id = vehicle["id"]
        name = build_vehicle_name(vehicle)

        self._attr_unique_id = f"{entry.entry_id}_vehicle_{vehicle_id}_status"
        self._attr_name = f"{name} Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"vehicle_{vehicle_id}")},
            name=name,
            manufacturer="LubeLogger",
            model=vehicle.get("model", "Vehicle"),
        )

    @property
    def native_value(self) -> str:
        """Return 'active' or 'sold'."""
        return "sold" if self._vehicle.get("soldDate") else "active"

    @property
    def extra_state_attributes(self):
        return {
            "sold_date": self._vehicle.get("soldDate"),
            "purchase_date": self._vehicle.get("purchaseDate"),
        }
