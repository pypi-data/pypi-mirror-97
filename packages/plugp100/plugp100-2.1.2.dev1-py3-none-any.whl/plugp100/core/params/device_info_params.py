import dataclasses
from dataclasses import dataclass
from typing import Optional


# TODO: improve this classes

@dataclass
class DeviceInfoParams:
    def as_dict(self):  # custom as_dict that remove None fields
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


@dataclass
class SwitchParams(DeviceInfoParams):
    device_on: Optional[bool]


@dataclass
class LightParams(SwitchParams):
    brightness: Optional[int]
