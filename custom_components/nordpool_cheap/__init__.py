"""Nordpool cheap slots integration."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

from .switch import CheapSlotSwitch
from .const import DOMAIN
from .price_fetcher import PriceFetcher

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via configuration.yaml."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True
    region = conf.get("region", "Europe/Stockholm")
    hours = conf.get("hours", 24)

    fetcher = PriceFetcher(hass, region, hours)
    hass.data[DOMAIN] = {
        "fetcher": fetcher,
        "switches": [],
    }

    one_hour = CheapSlotSwitch(fetcher, 1, "Cheap 1h Slot")
    three_hour = CheapSlotSwitch(fetcher, 3, "Cheap 3h Slot")
    hass.data[DOMAIN]["switches"].extend([one_hour, three_hour])

    async def refresh(_now):
        await fetcher.async_update()
        for entity in hass.data[DOMAIN]["switches"]:
            entity.async_schedule_update_ha_state(True)

    await fetcher.async_update()
    async_track_time_interval(hass, refresh, timedelta(hours=1))

    for entity in hass.data[DOMAIN]["switches"]:
        entity.hass = hass
        hass.async_create_task(entity.async_update_ha_state(True))

    return True
