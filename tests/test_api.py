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
    stations = sorted(get_stations(ws), key=lambda station: station.uic)
    assert len(stations) == 151
    assert stations[0].name == "Geltendorf"
    assert stations[0].uic == 8000119

    # TODO: Need to mock response from server
    assert stations[10].name == "Baldham"
    assert stations[10].uic == 8000785
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
