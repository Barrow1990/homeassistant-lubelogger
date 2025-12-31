from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LubeLogger sensors based on a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]
    vehicles = await api.get_vehicles()

    entities: list[SensorEntity] = []

    for vehicle in vehicles:
        entities.append(LubeLoggerVehicleStatusSensor(entry, vehicle))
        entities.append(LubeLoggerOdometerSensor(entry, vehicle))

    async_add_entities(entities)


def build_vehicle_name(vehicle: dict[str, Any]) -> str:
    """Create a readable vehicle name."""
    year = vehicle.get("year")
    make = vehicle.get("make", "")
    model = vehicle.get("model", "")

    parts = [str(year) if year else None, make, model]
    name = " ".join(p for p in parts if p)

    return name or f"Vehicle {vehicle['id']}"


class LubeLoggerVehicleStatusSensor(SensorEntity):
    """Main status sensor for a LubeLogger vehicle."""

    _attr_icon = "mdi:car-info"

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


class LubeLoggerOdometerSensor(SensorEntity):
    """Odometer sensor for a LubeLogger vehicle."""

    _attr_native_unit_of_measurement = "km"
    should_poll = True

    def __init__(self, entry: ConfigEntry, vehicle: dict[str, Any]):
        self._entry = entry
        self._vehicle = vehicle

        vehicle_id = vehicle["id"]
        name = build_vehicle_name(vehicle)

        self._attr_unique_id = f"{entry.entry_id}_vehicle_{vehicle_id}_odometer"
        self._attr_name = f"{name} Odometer"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"vehicle_{vehicle_id}")},
            name=name,
            manufacturer="LubeLogger",
            model=vehicle.get("model", "Vehicle"),
        )

        self._attr_native_value = None

    @property
    def available(self):
        return True


    async def async_update(self):
        """Fetch latest odometer value."""
        api = self.hass.data[DOMAIN][self._entry.entry_id]
        latest = await api.get_latest_odometer(self._vehicle["id"])
        self._attr_native_value = latest

    @property
    def extra_state_attributes(self):
        v = self._vehicle
        return {
            "vehicle_id": v.get("id"),
            "license_plate": v.get("licensePlate"),
            "year": v.get("year"),
            "make": v.get("make"),
            "model": v.get("model"),
            "purchase_date": v.get("purchaseDate"),
            "sold_date": v.get("soldDate"),
        }
