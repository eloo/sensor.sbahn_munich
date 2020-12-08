from datetime import date, datetime
import json

from custom_components.sbahn_munich.sensor import SBahnStation
from custom_components.sbahn_munich.api import Timetable, Station


def test_device_state_attributes():
    station = Station("testStation", [], "1235")
    entity = SBahnStation(station, None, None, None)

    line_dict = {
        "name": "S3",
        "color": "#333333",
        "text_color": "#444444",
    }

    timetable = []
    timetable.append(
        Timetable(
            line_dict,
            ris_estimated_time=datetime.now().timestamp() * 1000,
            ris_aimed_time=datetime.now().timestamp() * 1000,
            train_type=2,
            to="target1",
            updated_at=datetime.now().timestamp() * 1000,
        )
    )
    timetable.append(
        Timetable(
            line_dict,
            ris_estimated_time=datetime.now().timestamp() * 1000,
            ris_aimed_time=datetime.now().timestamp() * 1000,
            train_type=2,
            to="target2",
            updated_at=datetime.now().timestamp() * 1000,
        ),
    )
    entity._timetable = timetable
    attrributes = entity.device_state_attributes
    json.dumps(attrributes)
    assert attrributes != None
