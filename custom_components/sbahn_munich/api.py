from websocket import create_connection, WebSocketTimeoutException
import socket
import logging
import json
from datetime import datetime
from custom_components.sbahn_munich.const import (
    CMD_GET_STATIONS,
    CMD_GET_NEWSTICKER,
    CMD_GET_TIMETABLE_TPL,
)

_LOGGER = logging.getLogger(__name__)


class Station:
    def __init__(self, name, networkLines, uic, *args, **kwargs):
        self.name = name
        self.network_lines = []
        for line in networkLines:
            self.network_lines.append(Network_Line(**line))
        self.uic = uic
        self.timetable = None

    def __str__(self):
        return "{{name: {}, uic: {}, network_lines: {}}}".format(
            self.name, self.uic, self.network_lines
        )


class Network_Line:
    def __init__(self, name, color, text_color, *args, **kwargs):
        self.name = name
        self.color = color
        self.text_color = text_color

    def __str__(self):
        return "{{name: {}, color: {}, text_color: {}}}".format(
            self.name, self.color, self.text_color
        )


class Timetable:
    def __init__(
        self, line, ris_estimated_time, ris_aimed_time, train_type, to, *args, **kwargs
    ):
        self.line = Network_Line(**line)
        self.aimed_departure = datetime.fromtimestamp(ris_aimed_time / 1000.0)
        if ris_estimated_time:
            self.estimated_departure = datetime.fromtimestamp(
                ris_estimated_time / 1000.0
            )
        else:
            self.estimated_departure = None

        self.destination = to[0]
        self.train_type = train_type
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        estimated = None
        if self.estimated_departure:
            estimated = (self.estimated_departure.isoformat(),)
        return "{{line: {}, destination: {}, aimed: {}, estimated: {}, train_type: {}}}".format(
            self.line.name,
            self.destination,
            self.aimed_departure.isoformat(),
            estimated,
            self.train_type,
        )

    def sensor_attributes(self):
        value = {"destination": self.destination, "linename": self.line.name}
        if self.estimated_departure:
            value["time"] = self.estimated_departure - datetime.now().replace(
                second=0, microsecond=0
            )
        else:
            value["time"] = self.aimed_departure - datetime.now().replace(
                second=0, microsecond=0
            )
        value["raw_time"] = value["time"].total_seconds()
        value["time"] = value["time"].total_seconds() / 60
        value["product"] = "S-Bahn"
        if not self.kwargs["updated_at"]:
            self.kwargs["updated_at"] = 0
        value["updated_at"] = self.kwargs["updated_at"]
        return value


def get_stations(ws):
    return send_command(ws, CMD_GET_STATIONS)


def get_newsticket(ws):
    return send_command(ws, CMD_GET_NEWSTICKER)


def get_timetable(ws, station_code):
    cmd = CMD_GET_TIMETABLE_TPL.format(station_code)
    return send_command(ws, cmd)


def parse_data(data):
    parsed_data = json.loads(data)
    source = parsed_data["source"]
    if source == "station":
        return Station(**parsed_data["content"]["properties"])
    if str.startswith(source, "timetable_"):
        if parsed_data["content"]:
            return Timetable(**parsed_data["content"])


def open_websocket(uri, timeout):
    try:
        _LOGGER.debug("Open websocket: {}".format(uri))
        websocket = create_connection(uri, timeout=timeout)
        websocket.recv()
    except socket.timeout:
        _LOGGER.warning("Timeout while opening websocket")
        raise
    return websocket


def send_command(websocket, command):
    websocket.send(command)
    response = []
    while True:
        try:
            data = websocket.recv()
            response.append(parse_data(data))
        except WebSocketTimeoutException:
            break
    return response


def close_websocket(websocket):
    websocket.close()
    _LOGGER.debug("Websocket closed")
