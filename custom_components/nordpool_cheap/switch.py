"""Switches representing cheap slots."""

from datetime import timedelta
import datetime

from homeassistant.components.switch import SwitchEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN

class CheapSlotSwitch(SwitchEntity):
    """Switch that is on during the cheapest slot."""

    def __init__(self, fetcher, hours: int, name: str) -> None:
        self._fetcher = fetcher
        self._hours = hours
        self._name = name
        self._start: datetime.datetime | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool:
        if self._start is None:
            return False
        end = self._start + timedelta(hours=self._hours)
        now = dt_util.now()
        return self._start <= now < end

    async def async_update(self) -> None:
        await self._fetcher.async_update()
        if self._hours == 1:
            self._start = self._fetcher.cheapest_1h_start
        else:
            self._start = self._fetcher.cheapest_3h_start

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the switches."""
    data = hass.data.get(DOMAIN)
    if not data:
        return
    async_add_entities(data["switches"], True)
