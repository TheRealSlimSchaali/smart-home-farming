"""Garden data management for Smart Home Farming."""
import logging
from typing import Dict, List, Optional
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}.garden_data"


class GardenData:
    """Class to manage garden data storage."""

    def __init__(self, hass: HomeAssistant):
        """Initialize garden data."""
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data: Dict = {}

    async def async_load(self) -> None:
        """Load data from storage."""
        stored = await self._store.async_load()
        if stored:
            self._data = stored
        else:
            self._data = {
                "plants": [],
                "planting_records": [],
                "harvest_records": [],
                "planting_plans": [],
            }

    async def async_save(self) -> None:
        """Save data to storage."""
        await self._store.async_save(self._data)

    async def add_planting_plan(self, plan: Dict) -> None:
        """Add a new planting plan."""
        self._data["planting_plans"].append({
            "created_at": datetime.now().isoformat(),
            **plan
        })
        await self.async_save()

    async def add_planting_record(self, record: Dict) -> None:
        """Add a new planting record."""
        self._data["planting_records"].append({
            "created_at": datetime.now().isoformat(),
            **record
        })
        await self.async_save()

    async def add_harvest_record(self, record: Dict) -> None:
        """Add a new harvest record."""
        self._data["harvest_records"].append({
            "created_at": datetime.now().isoformat(),
            **record
        })
        await self.async_save()

    def get_planting_plans(self) -> List[Dict]:
        """Get all planting plans."""
        return self._data["planting_plans"]

    def get_planting_records(self) -> List[Dict]:
        """Get all planting records."""
        return self._data["planting_records"]

    def get_harvest_records(self) -> List[Dict]:
        """Get all harvest records."""
        return self._data["harvest_records"]
