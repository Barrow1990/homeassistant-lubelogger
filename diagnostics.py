from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
):
    """Return diagnostics for a config entry."""

    api = hass.data[DOMAIN][entry.entry_id]

    diagnostics = {
        "config_entry": {
            "title": entry.title,
            "data": entry.data,
            "options": entry.options,
        },
        "api": {
            "base_url": entry.data.get("base_url"),
            "auth_mode": "basic" if entry.data.get("username") else "none",
            "last_error": getattr(api.vehicles, "_last_error", None),
        },
        "vehicles": [],
    }

    try:
        vehicles = await api.vehicles.vehicles_list()
        diagnostics["vehicles"] = vehicles
    except Exception as err:
        diagnostics["vehicles_error"] = str(err)

    return diagnostics
