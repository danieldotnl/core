"""Support for ESPHome binary sensors."""
from __future__ import annotations

from aioesphomeapi import BinarySensorInfo, BinarySensorState

from homeassistant.components.binary_sensor import BinarySensorEntity

from . import EsphomeEntity, platform_async_setup_entry


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up ESPHome binary sensors based on a config entry."""
    await platform_async_setup_entry(
        hass,
        entry,
        async_add_entities,
        component_key="binary_sensor",
        info_type=BinarySensorInfo,
        entity_type=EsphomeBinarySensor,
        state_type=BinarySensorState,
    )


class EsphomeBinarySensor(EsphomeEntity, BinarySensorEntity):
    """A binary sensor implementation for ESPHome."""

    @property
    def _static_info(self) -> BinarySensorInfo:
        return super()._static_info

    @property
    def _state(self) -> BinarySensorState | None:
        return super()._state

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self._static_info.is_status_binary_sensor:
            # Status binary sensors indicated connected state.
            # So in their case what's usually _availability_ is now state
            return self._entry_data.available
        if self._state is None:
            return None
        if self._state.missing_state:
            return None
        return self._state.state

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return self._static_info.device_class

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if self._static_info.is_status_binary_sensor:
            return True
        return super().available
