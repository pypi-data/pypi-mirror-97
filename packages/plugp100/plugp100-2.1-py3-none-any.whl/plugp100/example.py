from plugp100.p100 import TapoSwitch, TapoLight

if __name__ == "__main__":
    # create plug
    sw = TapoSwitch("<ip>", "<email>", "<passwd>")
    sw.login()
    sw.off()
    print(sw.get_state())

    # create light
    light = TapoLight("<ip>", "<email>", "<passwd>")
    light.login()
    light.on()
    light.set_brightness(100)