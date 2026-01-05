from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry

from ..const import DOMAIN
from .utils import build_vehicle_name


class LubeLoggerVehicleInfoSensor(SensorEntity):
    """Metadata sensor for a LubeLogger vehicle."""

    _attr_icon = "mdi:car"
    _attr_has_entity_name = True
    _attr_translation_key = "vehicle_info"
    _attr_entity_category = None
    _attr_device_class = "lubelogger_vehicle_info"
    _attr_should_poll = False
    _attr_entity_registry_enabled_default = True
    _attr_primary = True

    def __init__(self, entry: ConfigEntry, vehicle: dict[str, Any]):
        self._entry = entry
        self._vehicle = vehicle

        vehicle_id = vehicle["id"]
        name = build_vehicle_name(vehicle)

        self._attr_unique_id = f"{entry.entry_id}_vehicle_{vehicle_id}_info"
        self._attr_name = name

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"vehicle_{vehicle_id}")},
            name=name,
            manufacturer="LubeLogger",
            model=vehicle.get("model", "Vehicle"),
        )

        # Info sensors have no meaningful primary value
        self._attr_native_value = "info"

    @property
    def extra_state_attributes(self):
        v = self._vehicle
        return {
            "vehicle_id": v.get("id"),
            "year": v.get("year"),
            "make": v.get("make"),
            "model": v.get("model"),
            "license_plate": v.get("licensePlate"),
            "purchase_date": v.get("purchaseDate"),
            "sold_date": v.get("soldDate"),
            "currency": self._entry.options.get("currency", "£"),
            "odometer_multiplier": v.get("odometerMultiplier"),
            "odometer_difference": v.get("odometerDifference"),
        }
