"""Config flow for Smart Home Farming."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_LOCATION,
    CONF_BEDS,
    CONF_BED_TYPE,
    CONF_LENGTH,
    CONF_WIDTH,
    CONF_COLD_FRAME,
    CONF_SUNLIGHT,
    CONF_NAME,
    BED_TYPES,
    SUNLIGHT_TYPES,
    BED_TYPE_TRANSLATIONS,
    SUNLIGHT_TYPE_TRANSLATIONS
)

_LOGGER = logging.getLogger(__name__)

class SmartHomeFarmingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Smart Home Farming."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize the config flow."""
        self.data = {}
        self.beds = []
        self._bed_count = {
            "raised_bed": 0,
            "deep_bed": 0,
            "plant_pot": 0
        }

    def _get_translated_types(self, type_translations):
        """Get translated options based on user's language."""
        # Get current language, fallback to English if not found
        language = self.hass.config.language or "en"
        language = language if language in type_translations else "en"
        
        # Create a dict of internal value to translated display value
        return {k: type_translations[language][k] for k in type_translations[language]}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        # Get list of zones from Home Assistant
        zones = self.hass.states.async_entity_ids("zone")
        zone_names = [state.split(".")[1] for state in zones]
        
        if user_input is not None:
            self.data.update(user_input)
            return await self.async_step_add_bed()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_LOCATION): vol.In(zone_names),
                }
            ),
            errors=errors,
        )

    async def async_step_add_bed(self, user_input=None):
        """Handle adding a bed."""
        errors = {}
        
        # Get translated options
        bed_types = self._get_translated_types(BED_TYPE_TRANSLATIONS)
        sunlight_types = self._get_translated_types(SUNLIGHT_TYPE_TRANSLATIONS)
        
        if user_input is not None:
            if user_input.get("add_another", False):
                bed_type = user_input[CONF_BED_TYPE]
                self._bed_count[bed_type] += 1
                name = f"{bed_types[bed_type]} {self._bed_count[bed_type]}"
                
                bed_data = {
                    CONF_NAME: name,
                    CONF_BED_TYPE: bed_type,
                    CONF_LENGTH: user_input[CONF_LENGTH],
                    CONF_WIDTH: user_input[CONF_WIDTH],
                    CONF_COLD_FRAME: user_input[CONF_COLD_FRAME],
                    CONF_SUNLIGHT: user_input[CONF_SUNLIGHT],
                }
                self.beds.append(bed_data)
                return await self.async_step_add_bed()
            else:
                # Add the last bed if data was provided
                if CONF_BED_TYPE in user_input:
                    bed_type = user_input[CONF_BED_TYPE]
                    self._bed_count[bed_type] += 1
                    name = f"{bed_types[bed_type]} {self._bed_count[bed_type]}"
                    
                    bed_data = {
                        CONF_NAME: name,
                        CONF_BED_TYPE: bed_type,
                        CONF_LENGTH: user_input[CONF_LENGTH],
                        CONF_WIDTH: user_input[CONF_WIDTH],
                        CONF_COLD_FRAME: user_input[CONF_COLD_FRAME],
                        CONF_SUNLIGHT: user_input[CONF_SUNLIGHT],
                    }
                    self.beds.append(bed_data)
                
                # Save all data and create entry
                self.data[CONF_BEDS] = self.beds
                return self.async_create_entry(title="Smart Home Farming", data=self.data)

        return self.async_show_form(
            step_id="add_bed",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_BED_TYPE): vol.In(bed_types),
                    vol.Required(CONF_LENGTH): vol.Coerce(int),
                    vol.Required(CONF_WIDTH): vol.Coerce(int),
                    vol.Required(CONF_COLD_FRAME, default=False): bool,
                    vol.Required(CONF_SUNLIGHT): vol.In(sunlight_types),
                    vol.Required("add_another", default=True): bool,
                }
            ),
            description_placeholders={
                "beds_count": len(self.beds),
            },
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
        self.beds = config_entry.data.get(CONF_BEDS, []).copy()
        self._bed_count = {
            "raised_bed": 0,
            "deep_bed": 0,
            "plant_pot": 0
        }
        # Update bed count based on existing beds
        for bed in self.beds:
            bed_type = bed[CONF_BED_TYPE]
            count = int(bed[CONF_NAME].split()[-1])
            self._bed_count[bed_type] = max(self._bed_count[bed_type], count)

    def _get_translated_types(self, type_translations):
        """Get translated options based on user's language."""
        # Get current language, fallback to English if not found
        language = self.hass.config.language or "en"
        language = language if language in type_translations else "en"
        
        # Create a dict of internal value to translated display value
        return {k: type_translations[language][k] for k in type_translations[language]}

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_add_bed()

    async def async_step_add_bed(self, user_input=None):
        """Handle adding a bed in options."""
        errors = {}
        
        # Get translated options
        bed_types = self._get_translated_types(BED_TYPE_TRANSLATIONS)
        sunlight_types = self._get_translated_types(SUNLIGHT_TYPE_TRANSLATIONS)
        
        if user_input is not None:
            if user_input.get("add_another", False):
                bed_type = user_input[CONF_BED_TYPE]
                self._bed_count[bed_type] += 1
                name = f"{bed_types[bed_type]} {self._bed_count[bed_type]}"
                
                bed_data = {
                    CONF_NAME: name,
                    CONF_BED_TYPE: bed_type,
                    CONF_LENGTH: user_input[CONF_LENGTH],
                    CONF_WIDTH: user_input[CONF_WIDTH],
                    CONF_COLD_FRAME: user_input[CONF_COLD_FRAME],
                    CONF_SUNLIGHT: user_input[CONF_SUNLIGHT],
                }
                self.beds.append(bed_data)
                return await self.async_step_add_bed()
            else:
                # Add the last bed if data was provided
                if CONF_BED_TYPE in user_input:
                    bed_type = user_input[CONF_BED_TYPE]
                    self._bed_count[bed_type] += 1
                    name = f"{bed_types[bed_type]} {self._bed_count[bed_type]}"
                    
                    bed_data = {
                        CONF_NAME: name,
                        CONF_BED_TYPE: bed_type,
                        CONF_LENGTH: user_input[CONF_LENGTH],
                        CONF_WIDTH: user_input[CONF_WIDTH],
                        CONF_COLD_FRAME: user_input[CONF_COLD_FRAME],
                        CONF_SUNLIGHT: user_input[CONF_SUNLIGHT],
                    }
                    self.beds.append(bed_data)
                
                # Update config entry with new beds
                new_data = dict(self.config_entry.data)
                new_data[CONF_BEDS] = self.beds
                self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
                return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="add_bed",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_BED_TYPE): vol.In(bed_types),
                    vol.Required(CONF_LENGTH): vol.Coerce(int),
                    vol.Required(CONF_WIDTH): vol.Coerce(int),
                    vol.Required(CONF_COLD_FRAME, default=False): bool,
                    vol.Required(CONF_SUNLIGHT): vol.In(sunlight_types),
                    vol.Required("add_another", default=True): bool,
                }
            ),
            description_placeholders={
                "beds_count": len(self.beds),
            },
            errors=errors,
        )
