# Smart Home Farming

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

A Home Assistant custom integration that helps with planning and maintaining a hobby vegetable garden using AI assistance. This integration uses AI (Google Gemini) to help you plan your garden, track plantings and harvests, and get personalized plant care recommendations.

## Features

- 🌱 Generate AI-powered planting plans based on your available space and desired plants
- 📝 Record and track plantings and harvests
- 🤖 Get AI-assisted plant care recommendations
- 📊 Monitor your garden's status through Home Assistant
- 🌍 Location-aware recommendations for climate-appropriate planting

## Installation

### HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Search for "Smart Home Farming" in HACS
3. Click Install
4. Restart Home Assistant
5. Go to Configuration > Integrations
6. Click "+ ADD INTEGRATION"
7. Search for "Smart Home Farming"
8. Follow the configuration steps

### Manual Installation

1. Download the latest release from GitHub
2. Copy the `custom_components/smart_home_farming` directory to your Home Assistant `custom_components` directory
3. Follow steps 4-7 from the HACS installation

## Configuration

You will need:
- A Google Gemini API key (or other LLM service)
- Your garden's location (for climate-appropriate recommendations)

## Services

The integration provides the following services:

### `smart_home_farming.generate_planting_plan`
Generate an AI-powered planting plan.

Parameters:
- `available_space`: Description of your available garden space
- `desired_plants`: List of plants you want to grow
- `planting_date`: When you plan to start planting

### `smart_home_farming.record_planting`
Record when you plant something.

Parameters:
- `plant`: Name of the plant
- `location`: Where in your garden you planted it
- `date`: Planting date

### `smart_home_farming.record_harvest`
Record when you harvest something.

Parameters:
- `plant`: Name of the plant
- `date`: Harvest date
- `yield_amount`: How much you harvested

### `smart_home_farming.get_garden_status`
Get the current status of your garden, including all planting plans, planting records, and harvest records.

## Dependencies

- Home Assistant
- Google Generative AI Python package (`google-generativeai>=0.1.0`)

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License

## Links

[releases-shield]: https://img.shields.io/github/release/yourusername/smart-home-farming.svg
[releases]: https://github.com/yourusername/smart-home-farming/releases
[license-shield]: https://img.shields.io/github/license/yourusername/smart-home-farming.svg
