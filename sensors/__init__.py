from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .vehicle_info import LubeLoggerVehicleInfoSensor
from .vehicle_status import LubeLoggerVehicleStatusSensor
from .odometer import LubeLoggerOdometerSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LubeLogger sensors based on a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]
    vehicles = await api.vehicles.vehicles_list()

    entities = []

    for vehicle in vehicles:
        entities.append(LubeLoggerVehicleInfoSensor(entry, vehicle))
        entities.append(LubeLoggerVehicleStatusSensor(entry, vehicle))
        entities.append(LubeLoggerOdometerSensor(entry, vehicle, api))

    async_add_entities(entities)
