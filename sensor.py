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
        entities.append(LubeLoggerVehicleOdometerSensor(entry, vehicle))

    async_add_entities(entities)


class LubeLoggerVehicleOdometerSensor(SensorEntity):
    """Odometer (or usage) sensor for a LubeLogger vehicle."""

    _attr_native_unit_of_measurement = "km"  # adjust later if needed

    def __init__(self, entry: ConfigEntry, vehicle: dict[str, Any]) -> None:
        self._entry = entry
        self._vehicle = vehicle

        vehicle_id = vehicle["id"]
        year = vehicle.get("year")
        make = vehicle.get("make", "")
        model = vehicle.get("model", "")

        name_parts = [str(year) if year else None, make, model]
        name = " ".join(p for p in name_parts if p)

        if not name:
            name = f"Vehicle {vehicle_id}"

        self._attr_unique_id = f"{entry.entry_id}_vehicle_{vehicle_id}_odometer"
        self._attr_name = f"{name} Odometer"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"vehicle_{vehicle_id}")},
            name=name,
            manufacturer="LubeLogger",
            model=model or "Vehicle",
            sw_version=None,
        )

    @property
    def available(self) -> bool:
        """Mark entity unavailable if the vehicle is sold."""
        sold_date = self._vehicle.get("soldDate")
        # If soldDate is null -> active; if not null -> sold
        return sold_date is None

    @property
    def native_value(self) -> float | None:
        """Return the odometer value.

        NOTE: Your /api/vehicles JSON doesn't include odometer yet.
        Once you know where odometer lives (another endpoint or field),
        update this to read it from self._vehicle or a coordinator.
        """
        # Placeholder until we wire in real odometer data:
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose extra useful info about the vehicle."""
        v = self._vehicle

        return {
            "vehicle_id": v.get("id"),
            "license_plate": v.get("licensePlate"),
            "year": v.get("year"),
            "make": v.get("make"),
            "model": v.get("model"),
            "purchase_date": v.get("purchaseDate"),
            "sold_date": v.get("soldDate"),
            "purchase_price": v.get("purchasePrice"),
            "sold_price": v.get("soldPrice"),
            "is_electric": v.get("isElectric"),
            "is_diesel": v.get("isDiesel"),
            "odometer_optional": v.get("odometerOptional"),
            "has_odometer_adjustment": v.get("hasOdometerAdjustment"),
        }
