# Plug P100
This is a fork of original work of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python)

The purpose of this fork is to provide the library as PyPi package. 

# How to install
```pip install plugp100```

# Code example
```python
from plugp100 import TapoApi, TapoSwitch, TapoLight
from plugp100.core.params import SwitchParams, LightParams

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

```

