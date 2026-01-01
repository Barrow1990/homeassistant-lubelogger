import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class LubeLoggerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial config flow for LubeLogger."""

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Create the config entry with user selections
            return self.async_create_entry(
                title="LubeLogger",
                data={
                    "base_url": user_input["base_url"],
                    "username": user_input.get("username"),
                    "password": user_input.get("password"),
                    "odometer_unit": user_input.get("odometer_unit", "km"),
                    "currency": user_input.get("currency", "£"),
                },
            )

        # Initial setup form
        data_schema = vol.Schema({
            vol.Required("base_url"): str,
            vol.Optional("username"): str,
            vol.Optional("password"): str,

            vol.Required(
                "odometer_unit",
                default="km"
            ): vol.In({
                "km": "Metric (KM)",
                "mi": "Imperial (Miles)"
            }),

            vol.Required(
                "currency",
                default="£"
            ): vol.In({
                "€": "Euro (€)",
                "$": "Dollars ($)",
                "£": "Pounds (£)"
            }),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(entry):
        """Return the options flow handler."""
        return LubeLoggerOptionsFlow(entry)


class LubeLoggerOptionsFlow(config_entries.OptionsFlow):
    """Handle options for LubeLogger (editable after setup)."""

    def __init__(self, entry: config_entries.ConfigEntry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # Update config entry with new values
            new_data = {**self.entry.data}
            new_data["odometer_unit"] = user_input["odometer_unit"]
            new_data["currency"] = user_input["currency"]

            self.hass.config_entries.async_update_entry(
                self.entry,
                data=new_data
            )

            return self.async_create_entry(title="", data={})

        # Options form (pre-filled with current values)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "odometer_unit",
                    default=self.entry.data.get("odometer_unit", "km")
                ): vol.In({
                    "km": "Metric (KM)",
                    "mi": "Imperial (Miles)"
                }),

                vol.Required(
                    "currency",
                    default=self.entry.data.get("currency", "£")
                ): vol.In({
                    "€": "Euro (€)",
                    "$": "Dollars ($)",
                    "£": "Pounds (£)"
                }),
            })
        )
