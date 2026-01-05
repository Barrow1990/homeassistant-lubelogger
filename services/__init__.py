from __future__ import annotations

from . import odometer, service_records, fuel


async def async_register_services(hass, entry, api):
    await odometer.register(hass, entry, api)
    await service_records.register(hass, entry, api)
    await fuel.register(hass, entry, api)
