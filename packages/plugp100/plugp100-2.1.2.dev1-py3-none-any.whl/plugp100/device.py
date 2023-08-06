from plugp100 import TapoApi, TapoDeviceState
from plugp100.core.params import SwitchParams, LightParams


class TapoDevice:

    def __init__(self, address: str, username: str, password: str):
        self.api = TapoApi(address)
        self.username = username
        self.password = password

    def login(self):
        self.api.login(self.username, self.password)

    def get_state(self) -> TapoDeviceState:
        return self.api.get_state()


class TapoSwitch(TapoDevice):
    def __init__(self, address: str, username: str, password: str):
        super().__init__(address, username, password)

    def on(self):
        self.api.set_device_info(SwitchParams(True))  # TODO: check response and use retry policy

    def off(self):
        self.api.set_device_info(SwitchParams(False))


# TODO: add support for color
class TapoLight(TapoSwitch):
    def __init__(self, address: str, username: str, password: str):
        super().__init__(address, username, password)

    def set_brightness(self, brightness: int):
        self.api.set_device_info(LightParams(None, brightness))