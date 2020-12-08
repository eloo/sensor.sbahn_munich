"""Platform for sensor integration."""
import logging
from datetime import timedelta
from operator import itemgetter

from homeassistant.const import TIME_MINUTES

from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from . import api
from .const import (
    ICON,
    DOMAIN,
    CONF_API_KEY,
    CONF_LINES,
    CONF_STATIONS,
    CONF_WS_TIMEOUT,
    DEFAULT_API_ENDPOINT_TPL,
    DEFAULT_API_KEY,
    DEFAULT_WS_TIMEOUT,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STATIONS): cv.ensure_list,
        vol.Optional(CONF_WS_TIMEOUT, default=DEFAULT_WS_TIMEOUT): cv.positive_float,
        vol.Optional(CONF_API_KEY, default=DEFAULT_API_KEY): cv.string,
        vol.Optional(CONF_LINES, default=[]): cv.ensure_list,
    }
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SBahn Munich platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    station_configs = config.get(CONF_STATIONS)
    api_key = config.get(CONF_API_KEY)
    lines = config.get(CONF_LINES)
    timeout = config.get(CONF_WS_TIMEOUT)

    uri = DEFAULT_API_ENDPOINT_TPL.format(api_key)

    ws = api.open_websocket(uri, timeout)

    stations = api.get_stations(ws)

    stations = list(
        filter(lambda x: x.name.lower() in map(str.lower, station_configs), stations)
    )

    api.close_websocket(ws)

    # Add devices
    add_entities(SBahnStation(station, lines, uri, timeout) for station in stations)


class SBahnStation(Entity):
    """Representation of a sbahn station sensor."""

    def __init__(self, station, lines, uri, timeout):
        """Initialize the sensor."""
        self._name = station.name
        self._state = None
        self._lines = lines
        self._uic = station.uic
        self._icon = ICON
        self._timetable = None
        self._uri = uri
        self._timeout = timeout

    @property
    def name(self):
        """Return the name of the sensor."""
        return DOMAIN + "_" + self._name

    @property
    def state(self):
        """Return the next departure time."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        timetables = self._timetable
        if not timetables:
            return None
        attr = {}
        attr["station"] = self._name
        departures = map(lambda x: x.sensor_attributes(), timetables)
        departures = list(filter(lambda x: x["raw_time"] >= 0, departures))
        attr["departures"] = sorted(
            departures, key=itemgetter("raw_time", "updated_at")
        )[:10]
        # attr["departures"] = sorted(departures, key=lambda x: x["departure"])[:10]
        return attr

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return TIME_MINUTES

    def update(self):
        """Get the latest data and update the state."""
        ws = api.open_websocket(self._uri, self._timeout)
        self._timetable = api.get_timetable(ws, self._uic)
        api.close_websocket(ws)
        self._state = self._timetable[0].aimed_departure
