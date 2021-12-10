"""This component provides support for a virtual switch."""

import logging

import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONF_NAME = "name"
CONF_INITIAL_VALUE = "initial_value"
CONF_INITIAL_AVAILABILITY = "initial_availability"

DEFAULT_INITIAL_VALUE = "off"
DEFAULT_INITIAL_AVAILABILITY = True

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_INITIAL_VALUE, default=DEFAULT_INITIAL_VALUE): cv.string,
        vol.Optional(
            CONF_INITIAL_AVAILABILITY, default=DEFAULT_INITIAL_AVAILABILITY
        ): cv.boolean,
    }
)


async def async_setup_platform(hass, config, async_add_entities, _discovery_info=None):
    """Write something."""
    switches = [VirtualSwitch(config)]
    async_add_entities(switches, True)


class VirtualSwitch(SwitchEntity):
    """Representation of a Virtual switch."""

    def __init__(self, config):
        """Initialize the Virtual switch device."""
        self._name = config.get(CONF_NAME)

        # Are we adding the domain or not?
        self.no_domain_ = self._name.startswith("!")
        if self.no_domain_:
            self._name = self.name[1:]
        self._unique_id = self._name.lower().replace(" ", "_")

        self._state = config.get(CONF_INITIAL_VALUE)
        self._available = config.get(CONF_INITIAL_AVAILABILITY)
        _LOGGER.info(f"VirtualSwitch: {self._name} created")

    @property
    def name(self):
        """Write something."""
        if self.no_domain_:
            return self._name
        else:
            return super().name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the switch."""
        return self._state

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.state == "on"

    @property
    def is_off(self):
        """Return true if switch is on."""
        return not self.is_on

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    def set_available(self, value):
        """Write something."""
        self._available = value
        self.async_schedule_update_ha_state()

    def turn_on(self, **kwargs):
        """Write something."""
        self._state = "on"

    def turn_off(self, **kwargs):
        """Write something."""
        self._state = "off"

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        attrs = {
            "friendly_name": self._name,
            "unique_id": self._unique_id,
        }
        return attrs
