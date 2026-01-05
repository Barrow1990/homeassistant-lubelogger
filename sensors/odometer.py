from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry

from ..const import DOMAIN
from .utils import build_vehicle_name


class LubeLoggerOdometerSensor(SensorEntity):
    """Odometer sensor for a LubeLogger vehicle."""

    _attr_primary = False
    _attr_should_poll = True

    def __init__(self, entry, vehicle, api):
        self._entry = entry
        self._vehicle = vehicle
        self._api = api

        vehicle_id = vehicle["id"]
        name = build_vehicle_name(vehicle)

        self._attr_unique_id = f"{entry.entry_id}_vehicle_{vehicle_id}_odometer"
        self._attr_name = f"{name} Odometer"

        # Unit from options, default to miles
        self._unit = entry.options.get("odometer_unit", "mi")
        self._attr_native_unit_of_measurement = self._unit

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"vehicle_{vehicle_id}")},
            name=name,
            manufacturer="LubeLogger",
            model=vehicle.get("model", "Vehicle"),
        )

        self._attr_native_value = None

        self._attr_extra_state_attributes = {}

        if self._api.odometer._last_error:
            self._attr_extra_state_attributes["last_api_error"] = self._api.odometer._last_error


    async def async_update(self) -> None:
        """Fetch latest odometer value."""
        api = self.hass.data[DOMAIN][self._entry.entry_id]
        latest = await self._api.odometer.get_latest_odometer(self._vehicle["id"])
        self._attr_native_value = latest

    @property
    def extra_state_attributes(self):
        return {
            "odometer_unit": self._unit,
        }
