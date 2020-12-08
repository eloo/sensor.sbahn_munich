from datetime import datetime
from freezegun import freeze_time

from . import line_dict

from custom_components.sbahn_munich.api import (
    Timetable,
    open_websocket,
    get_stations,
)

from custom_components.sbahn_munich.const import (
    DEFAULT_API_ENDPOINT_TPL,
    DEFAULT_API_KEY,
    DEFAULT_WS_TIMEOUT,
)


def test_get_stations():
    uri = DEFAULT_API_ENDPOINT_TPL.format(DEFAULT_API_KEY)
    ws = open_websocket(uri, DEFAULT_WS_TIMEOUT)
    stations = get_stations(ws)
    assert len(stations) == 149
    assert stations[0].name == "Starnberg Nord"
    assert stations[0].uic == 8005675

    # TODO: Need to mock response from server
    assert stations[10].name == "Geltendorf"
    assert stations[10].uic == 8000119
    assert len(stations[10].network_lines) == 2


@freeze_time("2020-12-07 21:09:01")
def test_time_should_be_zero():
    timetable = Timetable(
        line_dict,
        ris_estimated_time=datetime.fromisoformat("2020-12-07T21:09:00").timestamp()
        * 1000,
        ris_aimed_time=datetime.fromisoformat("2020-12-07T21:09:00").timestamp() * 1000,
        train_type=2,
        to="target1",
        updated_at=datetime.fromisoformat("2020-12-07T21:09:00").timestamp() * 1000,
    )
    attributes = timetable.sensor_attributes()
    assert attributes["time"] == 0
