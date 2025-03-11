"""The Smart Home Farming integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_LOCATION
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

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
from .garden_data import GardenData
from .llm_api import LLMApi

_LOGGER = logging.getLogger(__name__)

GENERATE_PLANTING_PLAN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_AVAILABLE_SPACE): cv.string,
        vol.Required(CONF_DESIRED_PLANTS): cv.ensure_list,
        vol.Required(CONF_PLANTING_DATE): cv.string,
    }
)

RECORD_PLANTING_SCHEMA = vol.Schema(
    {
        vol.Required("plant"): cv.string,
        vol.Required("location"): cv.string,
        vol.Required("date"): cv.string,
    }
)

RECORD_HARVEST_SCHEMA = vol.Schema(
    {
        vol.Required("plant"): cv.string,
        vol.Required("date"): cv.string,
        vol.Required("yield_amount"): cv.string,
    }
)

PLATFORMS = []

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Smart Home Farming component."""
    if DOMAIN in config:
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN]["config"] = config[DOMAIN]
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Home Farming from a config entry."""
    from .core import async_setup_entry as async_setup_core
    
    # Set up core functionality
    if not await async_setup_core(hass, entry):
        return False

    # Get the initialized components
    llm_api = hass.data[DOMAIN][entry.entry_id]["llm_api"]
    garden_data = hass.data[DOMAIN][entry.entry_id]["garden_data"]
    
    # Set up platforms
    if PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def generate_planting_plan(call):
        """Handle generate planting plan service call."""
        llm_api = hass.data[DOMAIN][entry.entry_id]["llm_api"]
        garden_data = hass.data[DOMAIN][entry.entry_id]["garden_data"]
        
        plan = await llm_api.generate_planting_plan(
            call.data[CONF_AVAILABLE_SPACE],
            call.data[CONF_DESIRED_PLANTS],
            call.data[CONF_PLANTING_DATE],
        )
        
        plan_data = {
            "plan": plan,
            "parameters": call.data
        }
        await garden_data.add_planting_plan(plan_data)
        return plan_data

    async def record_planting(call):
        """Handle record planting service call."""
        garden_data = hass.data[DOMAIN][entry.entry_id]["garden_data"]
        await garden_data.add_planting_record(call.data)
        return {"success": True, "record": call.data}

    async def record_harvest(call):
        """Handle record harvest service call."""
        garden_data = hass.data[DOMAIN][entry.entry_id]["garden_data"]
        await garden_data.add_harvest_record(call.data)
        return {"success": True, "record": call.data}

    async def get_garden_status(call):
        """Handle get garden status service call."""
        garden_data = hass.data[DOMAIN][entry.entry_id]["garden_data"]
        return {
            "planting_plans": garden_data.get_planting_plans(),
            "planting_records": garden_data.get_planting_records(),
            "harvest_records": garden_data.get_harvest_records(),
        }

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
        hass.services.async_remove(DOMAIN, service)

    # Unload core functionality
    from .core import async_unload_entry as async_unload_core
    return await async_unload_core(hass, entry)
