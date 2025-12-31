import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN
from .api import LubeLoggerAPI

DATA_SCHEMA = vol.Schema({
    vol.Required("base_url"): str,
    vol.Optional("username"): str,
    vol.Optional("password"): str,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LubeLogger."""

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            api = LubeLoggerAPI(
                user_input["base_url"],
                user_input.get("username"),
                user_input.get("password")
            )

            try:
                await api.get_vehicles()
                await api.close()
            except Exception:
                errors["base"] = "cannot_connect"

            else:
                return self.async_create_entry(
                    title="LubeLogger",
                    data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors
        )
