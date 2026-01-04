from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN
from .api import LubeLoggerApi

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up LubeLogger from a config entry."""

    base_url = entry.data["base_url"]
    username = entry.data.get("username")
    password = entry.data.get("password")

    # Create API client
    api = LubeLoggerApi(base_url, username, password)

    # Store API instance
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    # Reload integration when options change
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # -----------------------------
    # SERVICE HANDLERS
    # -----------------------------

    async def handle_add_odometer_entry(call: ServiceCall):
        """Add an odometer entry using a selected vehicle entity."""
        api: LubeLoggerApi = hass.data[DOMAIN][entry.entry_id]

        entity_id = call.data["entity_id"]
        value = call.data["value"]
        date = call.data["date"]

        state = hass.states.get(entity_id)
        if not state:
            _LOGGER.error("Entity %s not found", entity_id)
            return

        vehicle_id = state.attributes.get("vehicle_id")
        if not vehicle_id:
            _LOGGER.error("Entity %s has no vehicle_id attribute", entity_id)
            return

        _LOGGER.debug(
            "Adding odometer entry: entity=%s vehicle=%s value=%s date=%s",
            entity_id,
            vehicle_id,
            value,
            date,
        )

        await api.add_odometer_entry(vehicle_id, value, date)

    async def handle_add_service_record(call: ServiceCall):
        """Add a service record using a raw vehicle_id (for now)."""
        api: LubeLoggerApi = hass.data[DOMAIN][entry.entry_id]

        vehicle_id = call.data["vehicle_id"]
        data = call.data["data"]

        _LOGGER.debug(
            "Adding service record: vehicle=%s data=%s",
            vehicle_id,
            data,
        )

        await api.add_service_record(vehicle_id, data)

    async def handle_update_odometer_record(call: ServiceCall):
        """Update an odometer record using a raw vehicle_id (for now)."""
        api: LubeLoggerApi = hass.data[DOMAIN][entry.entry_id]

        vehicle_id = call.data["vehicle_id"]
        value = call.data["value"]
        date = call.data["date"]

        _LOGGER.debug(
            "Updating odometer record: vehicle=%s value=%s date=%s",
            vehicle_id,
            value,
            date,
        )

        await api.update_odometer_record(vehicle_id, value, date)

    # -----------------------------
    # REGISTER SERVICES
    # -----------------------------

    hass.services.async_register(
        DOMAIN,
        "add_odometer_entry",
        handle_add_odometer_entry,
    )

    hass.services.async_register(
        DOMAIN,
        "add_service_record",
        handle_add_service_record,
    )

    hass.services.async_register(
        DOMAIN,
        "update_odometer_record",
        handle_update_odometer_record,
    )

    # -----------------------------
    # LOAD PLATFORMS
    # -----------------------------

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug("LubeLogger integration initialized for %s", base_url)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a LubeLogger config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    api: LubeLoggerApi = hass.data[DOMAIN][entry.entry_id]
    await api.close()

    hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload integration when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
