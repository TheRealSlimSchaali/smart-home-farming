"""LLM API for Smart Home Farming."""
import logging
import google.generativeai as genai

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LLMApi:
    """LLM API for Smart Home Farming."""

    def __init__(self, api_key, location):
        """Initialize LLM API."""
        self.api_key = api_key
        self.location = location
        # Initialize the Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_planting_plan(self, available_space, desired_plants, planting_date):
        """Generate planting plan."""
        prompt = f"""As a gardening expert, create a planting plan for the following:
        - Available space: {available_space}
        - Desired plants: {', '.join(desired_plants)}
        - Planting date: {planting_date}
        - Location: {self.location}
        
        Consider:
        1. Companion planting benefits
        2. Space requirements for each plant
        3. Seasonal timing
        4. Local climate conditions
        5. Plant spacing and layout
        
        Provide a detailed plan including:
        - Plant placement recommendations
        - Timing for each plant
        - Care instructions
        """
        
        try:
            response = await self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            _LOGGER.error("Error generating planting plan: %s", str(e))
            return f"Error generating planting plan: {str(e)}"

    async def get_plant_care_recommendations(self, plant):
        """Get plant care recommendations."""
        prompt = f"""As a gardening expert, provide detailed care recommendations for {plant} in {self.location}.
        Include:
        1. Watering requirements
        2. Sunlight needs
        3. Soil preferences
        4. Common issues and solutions
        5. Harvesting tips (if applicable)
        """
        
        try:
            response = await self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            _LOGGER.error("Error getting plant care recommendations: %s", str(e))
            return f"Error getting plant care recommendations: {str(e)}"
