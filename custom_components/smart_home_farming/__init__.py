"""The Smart Home Farming integration."""
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_LOCATION
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    SERVICE_GENERATE_PLANTING_PLAN,
    SERVICE_RECORD_PLANTING,
    SERVICE_RECORD_HARVEST,
    SERVICE_GET_GARDEN_STATUS,
    CONF_AVAILABLE_SPACE,
    CONF_DESIRED_PLANTS,
    CONF_PLANTING_DATE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = []

# This integration only supports configuration via the UI
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

# Service schemas
GENERATE_PLANTING_PLAN_SCHEMA = vol.Schema({
    vol.Required(CONF_AVAILABLE_SPACE): cv.string,
    vol.Required(CONF_DESIRED_PLANTS): cv.ensure_list,
    vol.Optional(CONF_PLANTING_DATE): cv.string,
})

RECORD_PLANTING_SCHEMA = vol.Schema({
    vol.Required("plant"): cv.string,
    vol.Required("location"): cv.string,
    vol.Optional("date"): cv.string,
})

RECORD_HARVEST_SCHEMA = vol.Schema({
    vol.Required("plant"): cv.string,
    vol.Optional("date"): cv.string,
    vol.Optional("yield_amount"): cv.string,
})

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Smart Home Farming component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Home Farming from a config entry."""
    # Set up core functionality
    from .core import async_setup_entry as async_setup_core
    
    if not await async_setup_core(hass, entry):
        return False

    # Get the initialized components
    llm_api = hass.data[DOMAIN][entry.entry_id]["llm_api"]
    garden_data = hass.data[DOMAIN][entry.entry_id]["garden_data"]

    # Set up platforms
    if PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def generate_planting_plan(call: ServiceCall) -> None:
        """Handle generate planting plan service call."""
        _LOGGER.debug("Generating planting plan with parameters: %s", call.data)
        try:
            plan = await llm_api.generate_planting_plan(
                call.data[CONF_AVAILABLE_SPACE],
                call.data[CONF_DESIRED_PLANTS],
                call.data.get(CONF_PLANTING_DATE),
            )
            
            plan_data = {
                "plan": plan,
                "parameters": call.data
            }
            await garden_data.add_planting_plan(plan_data)
            _LOGGER.debug("Successfully generated and saved planting plan")
        except Exception as e:
            _LOGGER.error("Error generating planting plan: %s", str(e))
            raise

    async def record_planting(call: ServiceCall) -> None:
        """Handle record planting service call."""
        _LOGGER.debug("Recording planting with parameters: %s", call.data)
        try:
            await garden_data.add_planting_record(dict(call.data))
            _LOGGER.debug("Successfully recorded planting")
        except Exception as e:
            _LOGGER.error("Error recording planting: %s", str(e))
            raise

    async def record_harvest(call: ServiceCall) -> None:
        """Handle record harvest service call."""
        _LOGGER.debug("Recording harvest with parameters: %s", call.data)
        try:
            await garden_data.add_harvest_record(dict(call.data))
            _LOGGER.debug("Successfully recorded harvest")
        except Exception as e:
            _LOGGER.error("Error recording harvest: %s", str(e))
            raise

    async def get_garden_status(call: ServiceCall) -> dict:
        """Handle get garden status service call."""
        _LOGGER.debug("Getting garden status")
        try:
            return {
                "planting_plans": garden_data.get_planting_plans(),
                "planting_records": garden_data.get_planting_records(),
                "harvest_records": garden_data.get_harvest_records(),
            }
        except Exception as e:
            _LOGGER.error("Error getting garden status: %s", str(e))
            raise

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_PLANTING_PLAN,
        generate_planting_plan,
        schema=GENERATE_PLANTING_PLAN_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_RECORD_PLANTING,
        record_planting,
        schema=RECORD_PLANTING_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_RECORD_HARVEST,
        record_harvest,
        schema=RECORD_HARVEST_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_GARDEN_STATUS,
        get_garden_status,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    if PLATFORMS:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
        if not unload_ok:
            return False

    # Remove services
    for service in [
        SERVICE_GENERATE_PLANTING_PLAN,
        SERVICE_RECORD_PLANTING,
        SERVICE_RECORD_HARVEST,
        SERVICE_GET_GARDEN_STATUS,
    ]:
        if hass.services.has_service(DOMAIN, service):
            hass.services.async_remove(DOMAIN, service)

    # Unload core functionality
    from .core import async_unload_entry as async_unload_core
    return await async_unload_core(hass, entry)
