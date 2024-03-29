"""Constants for sbahn munich integration"""
# Base component constants
NAME = "SBahn Munich"
DOMAIN = "sbahn_munich"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.2"

# Icons
ICON = "mdi:train"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_STATIONS = "stations"
CONF_STATION_UICS = "stations_uics"
CONF_LINES = "lines"
CONF_LIMIT = "limit"
CONF_API_KEY = "apikey"
CONF_WS_TIMEOUT = "ws_timeout"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_API_ENDPOINT_TPL = "wss://api.geops.io/realtime-ws/v1/?key={}"
DEFAULT_WS_TIMEOUT = 0.5
DEFAULT_LIMIT = 5

# API commands
CMG_GET_HEALTHCHECK = "GET healthcheck"
CMD_GET_NEWSTICKER = "GET newsticker"
CMD_GET_STATIONS = "GET station"
CMD_GET_TIMETABLE_TPL = "GET timetable_{}"
