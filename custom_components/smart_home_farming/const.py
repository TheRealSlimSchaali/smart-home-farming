"""Constants for the Smart Home Farming integration."""

DOMAIN = "smart_home_farming"

# Configuration constants
CONF_API_KEY = "api_key"
CONF_LOCATION = "location"
CONF_BEDS = "beds"
CONF_BED_TYPE = "bed_type"
CONF_LENGTH = "length"
CONF_WIDTH = "width"
CONF_COLD_FRAME = "cold_frame"
CONF_SUNLIGHT = "sunlight"
CONF_NAME = "name"

# Bed types
BED_TYPE_RAISED = "raised_bed"
BED_TYPE_DEEP = "deep_bed"
BED_TYPE_POT = "plant_pot"
BED_TYPES = [BED_TYPE_RAISED, BED_TYPE_DEEP, BED_TYPE_POT]

# Bed type translations
BED_TYPE_TRANSLATIONS = {
    "en": {
        BED_TYPE_RAISED: "Raised Bed",
        BED_TYPE_DEEP: "Deep Bed",
        BED_TYPE_POT: "Plant Pot"
    },
    "de": {
        BED_TYPE_RAISED: "Hochbeet",
        BED_TYPE_DEEP: "Tiefbeet",
        BED_TYPE_POT: "Pflanzkübel"
    }
}

# Sunlight types
SUNLIGHT_DIRECT = "direct"
SUNLIGHT_INDIRECT = "indirect"
SUNLIGHT_TYPES = [SUNLIGHT_DIRECT, SUNLIGHT_INDIRECT]

# Sunlight type translations
SUNLIGHT_TYPE_TRANSLATIONS = {
    "en": {
        SUNLIGHT_DIRECT: "Direct Sunlight",
        SUNLIGHT_INDIRECT: "Indirect Sunlight"
    },
    "de": {
        SUNLIGHT_DIRECT: "Direkte Sonne",
        SUNLIGHT_INDIRECT: "Indirekte Sonne"
    }
}

# Storage
STORAGE_KEY = "garden_data"
STORAGE_VERSION = 1

# Services
SERVICE_GENERATE_PLANTING_PLAN = "generate_planting_plan"
SERVICE_RECORD_PLANTING = "record_planting"
SERVICE_RECORD_HARVEST = "record_harvest"
SERVICE_GET_GARDEN_STATUS = "get_garden_status"

# Service parameters
CONF_AVAILABLE_SPACE = "available_space"
CONF_DESIRED_PLANTS = "desired_plants"
CONF_PLANTING_DATE = "planting_date"
