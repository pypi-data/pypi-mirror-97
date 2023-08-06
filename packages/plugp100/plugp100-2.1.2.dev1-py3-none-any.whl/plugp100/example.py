from plugp100 import TapoApi
from plugp100.core.params import SwitchParams, LightParams

if __name__ == "__main__":
    # create generic tapo api
    sw = TapoApi("<ip>")
    sw.login("<email>", "<passwd>")
    sw.set_device_info(SwitchParams(True))
    sw.set_device_info(LightParams(None, 100))
    print(sw.get_state())

    # create specific switch or light
    # sw = TapoSwitch("<ip>", "<email>", "<passwd>")
    # sw.on()
    # lg = TapoLight("<ip>", "<email>", "<passwd>")
    # lg.set_brightness(100)
