"""
Firmware   | LAN type  | uiid | Product Model
-----------|-----------|------|--------------
ITA-GZ1-GL | plug      | 14   | Sonoff (Sonoff Basic)
PSF-B01-GL | plug      | 1    | - (switch 1ch)
PSF-BD1-GL | plug      | 1    | MINI (Sonoff Mini)
PSF-B04-GL | strip     | 2    | - (switch 2ch)
PSF-B04-GL | strip     | 4    | 4CHPRO (Sonoff 4CH Pro)
"""
import logging
from typing import Optional

from homeassistant.helpers.entity import ToggleEntity

from . import DOMAIN
from .sonoff_main import EWeLinkRegistry, EWeLinkDevice


async def async_setup_platform(hass, config, add_entities,
                               discovery_info=None):
    if discovery_info is None:
        return

    deviceid = discovery_info['deviceid']
    channels = discovery_info['channels']
    registry = hass.data[DOMAIN]
    add_entities([EWeLinkToggle(registry, deviceid, channels)])


_LOGGER = logging.getLogger(__name__)


class EWeLinkToggle(ToggleEntity, EWeLinkDevice):
    def __init__(self, registry: EWeLinkRegistry, deviceid: str,
                 channels: list = None):
        self.registry = registry
        self.deviceid = deviceid
        self.channels = channels

    async def async_added_to_hass(self) -> None:
        self._init()

    def _update_handler(self, state: dict, attrs: dict):
        self._attrs.update(attrs)

        # TODO: handle online
        # if 'online' in state:
        #     self._available = state['online']

        if 'switch' in state or 'switches' in state:
            self._is_on = any(self._is_on_list(state))

        self.schedule_update_ha_state()

    @property
    def should_poll(self) -> bool:
        # The device itself sends an update of its status
        return False

    @property
    def unique_id(self) -> Optional[str]:
        if self.channels:
            chid = ''.join(str(ch) for ch in self.channels)
            return f'{self.deviceid}_{chid}'
        else:
            return self.deviceid

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def supported_features(self):
        return 0

    @property
    def state_attributes(self):
        return self._attrs

    @property
    def available(self) -> bool:
        return self._available

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        await self._turn_on()

    async def async_turn_off(self, **kwargs) -> None:
        await self._turn_off()
