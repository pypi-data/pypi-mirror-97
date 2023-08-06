# Plug P100
This is a fork of original work of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python)

The purpose of this fork is to provide the library as PyPi package. 

# How to install
```pip install plugp100```

# Code example
```python
from plugp100 import TapoSwitch, TapoLight

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
```

