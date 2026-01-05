from __future__ import annotations
from homeassistant.core import HomeAssistant, ServiceCall
from ..const import DOMAIN


async def register(hass: HomeAssistant, entry, api):

    async def handle_add(call: ServiceCall):
        entity_id = call.data["entity_id"]
        value = call.data["value"]
        date = call.data["date"]

        state = hass.states.get(entity_id)
        vehicle_id = state.attributes.get("vehicle_id")

        await api.odometer.add(vehicle_id, value, date)

    hass.services.async_register(
        DOMAIN,
        "add_odometer_entry",
        handle_add,
    )
