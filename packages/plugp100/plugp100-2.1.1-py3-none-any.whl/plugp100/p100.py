import base64
import dataclasses
import json
from dataclasses import dataclass
from typing import Any, Dict

from plugp100.core.api import TapoApi
from plugp100.core.params import SwitchParams, LightParams

TERMINAL_UUID = "88-00-DE-AD-52-E1"


@dataclass
class TapoDeviceState:
    nickname: str = property(lambda self: base64.b64decode(self.state["nickname"]).decode("UTF-8"))
    model: str = property(lambda self: self.state["model"])
    type: str = property(lambda self: self.state["type"])
    device_on: bool = property(lambda self: self.state["device_on"])
    overheated: bool = property(lambda self: self.state["overheated"])
    signal_level: int = property(lambda self: self.state["signal_level"])
    rssi: int = property(lambda self: self.state["rssi"])

    def __init__(self, state: Dict[str, Any]):
        self.state = state


class TapoDevice:
    def __init__(self, address: str, username: str, password: str):
        self.api = TapoApi(address)
        self.username = username
        self.password = password

    def login(self):
        self.api.handshake()
        self.api.login_request(self.username, self.password)

    def get_state(self) -> TapoDeviceState:
        return TapoDeviceState(self.api.get_state())


class TapoSwitch(TapoDevice):
    def __init__(self, address: str, username: str, password: str):
        super().__init__(address, username, password)

    def on(self):
        self.api.set_device_info(SwitchParams(True), TERMINAL_UUID)  # TODO: check response and use retry policy

    def off(self):
        self.api.set_device_info(SwitchParams(False), TERMINAL_UUID)


# TODO: add support for color
class TapoLight(TapoSwitch):
    def __init__(self, address: str, username: str, password: str):
        super().__init__(address, username, password)

    def set_brightness(self, brightness: int):
        self.api.set_device_info(LightParams(None, brightness), TERMINAL_UUID)


