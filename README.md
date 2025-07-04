# Nordpool Cheap Slots Home Assistant Integration

This custom component fetches electricity prices from Nordpool and exposes two
switches that turn on during the cheapest periods of the day.

* `switch.cheap_1h_slot` &ndash; turns on during the cheapest single hour.
* `switch.cheap_3h_slot` &ndash; turns on during the cheapest three consecutive hours.

## Installation

Copy the `custom_components/nordpool_cheap` directory to your Home Assistant
`config/custom_components` folder.

Add the following to your `configuration.yaml` and restart Home Assistant:

```yaml
nordpool_cheap:
  region: "Europe/Stockholm"
```

Use these switches to trigger automations when electricity prices are low.
