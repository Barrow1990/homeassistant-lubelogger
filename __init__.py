from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_BASE_URL, CONF_USERNAME, CONF_PASSWORD
from .api import LubeLoggerApi
from .services import async_register_services

import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Setting up LubeLogger integration")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up LubeLogger from a config entry."""
    base_url = entry.data[CONF_BASE_URL]
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    api = LubeLoggerApi(base_url, username, password)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    await async_register_services(hass, entry, api)

    # Modern HA method
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a LubeLogger config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
