# Plug P100
This is a fork of original work of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python)

The purpose of this fork is to provide the library as PyPi package. 

# How to install
```pip install plugp100```

# Code example

```python
import asyncio
from plugp100 import TapoApiClient


async def main():
    # create generic tapo api
    sw = TapoApiClient("<ip>", "<email>", "<passwd>")
    await sw.login()
    await sw.on()
    await sw.set_brightness(100)
    print(await sw.get_state())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(0.1))
loop.close()

```

