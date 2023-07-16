from dataclasses import dataclass
from datetime import datetime

government_date_format = "%Y-%m-%dT%H:%M"


@dataclass
class Appointment:
    locationId: int
    startTimestamp: datetime
    endTimestamp: datetime
    active: bool
    duration: int
    remoteInd: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["locationId"],
            datetime.strptime(data["startTimestamp"], government_date_format),
            datetime.strptime(data["endTimestamp"], government_date_format),
            data["active"],
            data["duration"],
            data["remoteInd"],
        )
