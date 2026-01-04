"""Constants for the LubeLogger integration."""

DOMAIN = "lubelogger"

# Integration metadata
NAME = "LubeLogger"
VERSION = "1.0.0"

# Config entry keys
CONF_BASE_URL = "base_url"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_ODOMETER_UNIT = "odometer_unit"
CONF_CURRENCY = "currency"

# Default values
DEFAULT_ODOMETER_UNIT = "mi"
DEFAULT_CURRENCY = "£"

# Supported units
ODOMETER_UNITS = {
    "km": "Metric (KM)",
    "mi": "Imperial (Miles)",
}

# Supported currencies
CURRENCIES = {
    "€": "Euro (€)",
    "$": "Dollars ($)",
    "£": "Pounds (£)",
}

# Platforms
PLATFORMS = ["sensor"]
