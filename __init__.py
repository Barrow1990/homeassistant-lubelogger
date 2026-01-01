from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .api import LubeLoggerApi

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload when options change."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up LubeLogger from a config entry."""

    base_url = entry.data["base_url"]
    username = entry.data.get("username")
    password = entry.data.get("password")

    # Create API client
    api = LubeLoggerApi(base_url, username, password)

    # Store API instance for this entry
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    # Update listener to handle config changes
    entry.async_on_unload(
        entry.add_update_listener(async_reload_entry)
    )


    # Forward setup to platforms (sensor.py)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug("LubeLogger integration initialized for %s", base_url)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a LubeLogger config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Close API session
    api: LubeLoggerApi = hass.data[DOMAIN][entry.entry_id]
    await api.close()

    # Remove stored data
    hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
