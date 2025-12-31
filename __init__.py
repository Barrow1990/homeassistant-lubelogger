from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .api import LubeLoggerAPI

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up LubeLogger from a config entry."""

    api = LubeLoggerAPI(
        entry.data["base_url"],
        entry.data.get("username"),   # <-- FIXED
        entry.data.get("password")    # <-- FIXED
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload LubeLogger."""

    api = hass.data[DOMAIN].pop(entry.entry_id)
    await api.close()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok
