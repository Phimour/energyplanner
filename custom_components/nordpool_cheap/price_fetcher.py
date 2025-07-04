"""Fetch prices from Nordpool and compute cheap slots."""

import datetime
from datetime import timedelta
from typing import List

from homeassistant.util import dt as dt_util
from homeassistant.core import HomeAssistant
from nordpool import elspot

class PriceFetcher:
    """Fetch Nordpool prices and compute cheapest slots."""

    def __init__(self, hass: HomeAssistant, region: str, hours: int = 24) -> None:
        self.hass = hass
        self.region = region
        self.hours = hours
        self.prices: List[float] = []
        self.cheapest_1h_start: datetime.datetime | None = None
        self.cheapest_3h_start: datetime.datetime | None = None

    def _get_prices(self) -> List[float]:
        prices_spot = elspot.Prices()
        data = prices_spot.get_prices(self.region)
        today = data["today"]
        return [h["value"] for h in today][: self.hours]

    def _calculate_slots(self) -> None:
        if not self.prices:
            self.cheapest_1h_start = None
            self.cheapest_3h_start = None
            return
        start_day = dt_util.start_of_local_day()
        idx_min = self.prices.index(min(self.prices))
        self.cheapest_1h_start = start_day + timedelta(hours=idx_min)
        best_avg = None
        best_idx = 0
        for idx in range(len(self.prices) - 2):
            avg = sum(self.prices[idx : idx + 3]) / 3
            if best_avg is None or avg < best_avg:
                best_avg = avg
                best_idx = idx
        self.cheapest_3h_start = start_day + timedelta(hours=best_idx)

    async def async_update(self) -> None:
        self.prices = await self.hass.async_add_executor_job(self._get_prices)
        self._calculate_slots()
