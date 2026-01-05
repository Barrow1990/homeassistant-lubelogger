from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_BASE_URL,
    CONF_USERNAME,
    CONF_PASSWORD,
    DEFAULT_BASE_URL,
)


class LubeLoggerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for LubeLogger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Optional username/password logic preserved
            base_url = user_input.get(CONF_BASE_URL, DEFAULT_BASE_URL)
            username = user_input.get(CONF_USERNAME) or None
            password = user_input.get(CONF_PASSWORD) or None

            return self.async_create_entry(
                title="LubeLogger",
                data={
                    CONF_BASE_URL: base_url,
                    CONF_USERNAME: username,
                    CONF_PASSWORD: password,
                },
            )

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
                vol.Optional(CONF_USERNAME): str,
                vol.Optional(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle YAML import."""
        return await self.async_step_user(user_input)
