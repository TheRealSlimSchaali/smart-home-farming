"""Core component logic for Smart Home Farming."""
import logging
import voluptuous as vol
from homeassistant.const import CONF_API_KEY, CONF_LOCATION
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_API_KEY): cv.string,
                vol.Required(CONF_LOCATION): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Smart Home Farming component from configuration.yaml."""
    conf = config.get(DOMAIN)

    if conf is None:
        return True

    hass.data[DOMAIN] = {
        CONF_API_KEY: conf[CONF_API_KEY],
        CONF_LOCATION: conf[CONF_LOCATION],
    }

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "import"}, data=conf
        )
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Smart Home Farming from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    location = entry.data[CONF_LOCATION]

    # Initialize services and data storage
    hass.data.setdefault(DOMAIN, {})

    # Initialize the LLM API
    from .llm_api import LLMApi
    llm_api = LLMApi(api_key, location)
    
    # Initialize garden data storage
    from .garden_data import GardenData
    garden_data = GardenData(hass)
    await garden_data.async_load()

    hass.data[DOMAIN][entry.entry_id] = {
        "llm_api": llm_api,
        "garden_data": garden_data,
    }

    _LOGGER.info("Setting up Smart Home Farming component with location: %s", location)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Clean up component data
    if entry.entry_id in hass.data[DOMAIN]:
        # Get the garden data instance
        garden_data = hass.data[DOMAIN][entry.entry_id].get("garden_data")
        if garden_data:
            # Save any pending data
            await garden_data.async_save()
        
        # Remove the entry data
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.info("Unloading Smart Home Farming component")
    return True
