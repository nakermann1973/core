"""The gogogate2 component."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .common import get_api, get_data_update_coordinator
from .const import DEVICE_TYPE_GOGOGATE2

PLATFORMS = [Platform.COVER, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Do setup of Gogogate2."""

    # Update the config entry.
    config_updates = {}
    if CONF_DEVICE not in entry.data:
        config_updates = {
            **entry.data,
            **{CONF_DEVICE: DEVICE_TYPE_GOGOGATE2},
        }

    if config_updates:
        hass.config_entries.async_update_entry(entry, data=config_updates)

    # Make initial connection to ensure the device is available
    api = get_api(hass, entry.data)
    try:
      rv = await api.async_info()
      # TODO: check for a valid return here
      _LOGGER.info("info returned: %s", rv)
    except Exception as ex:
      # TODO: Catch specific exception types here
      _LOGGER.error("Error connecting to gogogate: %s", ex)
      raise ConfigEntryNotReady("Connection to gogogate failed") from ex

    data_update_coordinator = get_data_update_coordinator(hass, entry)
    await data_update_coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Gogogate2 config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
