"""Config flow for Smart Home Farming."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LOCATION
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SmartHomeFarmingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Smart Home Farming."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Smart Home Farming", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_LOCATION): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return SmartHomeFarmingOptionsFlow(config_entry)


class SmartHomeFarmingOptionsFlow(config_entries.OptionsFlow):
    """Options flow handler for Smart Home Farming."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_API_KEY, default=self.config_entry.options.get(CONF_API_KEY, "")): str,
                    vol.Optional(CONF_LOCATION, default=self.config_entry.options.get(CONF_LOCATION, "")): str,
                }
            ),
            errors=errors,
        )
