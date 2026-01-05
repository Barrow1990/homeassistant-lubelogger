from __future__ import annotations
from homeassistant.core import HomeAssistant, ServiceCall
from ..const import DOMAIN


async def register(hass: HomeAssistant, entry, api):

    async def handle_add(call: ServiceCall):
        entity_id = call.data["entity_id"]
        data = call.data["data"]

        state = hass.states.get(entity_id)
        vehicle_id = state.attributes.get("vehicle_id")

        await api.fuel.add(vehicle_id, data)

    hass.services.async_register(
        DOMAIN,
        "add_fuel_record",
        handle_add,
    )
