# Mock.GPIO
Mock Library for RPI.GPIO python Library

Mock.GPIO is a python library that supports development of software/program and to debug them outside RPi (eg: ubuntu ). it can be intergrated along with any generic application/program/software.

it help in making your program/application run seamlessly both outside and inside RPi by
- Printing the intended actions (without GUI) for debugging, when executed outside RPi
- Works exactly as intended in an actual RPi without a need for code change.


The easiest way to use this package is to install using pip3 for python 3

```bash
$ sudo pip3 install Mock.GPIO
```

To import the Mock library at the beginning of your script, use

```python
from Mock.GPIO import GPIO
```

or

To enable seamless switching between Mock library when you are outside RPi and the actual RPi.GPIO library when you are inside RPi, use

```python

try:
    # checks if you have access to RPi.GPIO, which is available inside RPi
    import RPi.GPIO as GPIO
except:
    # In case of exception, It realises that, you are executing your script outside, so imports Mock.GPIO
    import Mock.GPIO as GPIO
```

## Works with

- [python 3.6.8](https://www.python.org/downloads/release/3.6.8)

## Simulation

This library simulates the following functions which are used in the RPi.GPIO library.

- GPIO.setmode()
- GPIO.getmode()
- GPIO.setwarnings()
- GPIO.setup()
- GPIO.output()
- GPIO.input()
- GPIO.wait_for_edge()
- GPIO.add_event_detect()
- GPIO.event_detected()
- GPIO.add_event_callback()
- GPIO.remove_event_detect()
- GPIO.gpio_function()
- GPIO.start()
- GPIO.ChangeFrequency()
- GPIO.ChangeDutyCycle()
- GPIO.stop()
- GPIO.cleanup()

### Usage:

``` python
import Mock.GPIO as GPIO
```

## Documentation

- [Library Overview](https://htmlpreview.github.io/?https://github.com/codenio/Mock.GPIO/blob/master/docs/Mock.GPIO.html)
- [Examples](examples)

### Example:

The following python example/test.py

```python

try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

import time

print ("set mode")
GPIO.setmode(GPIO.BCM)
print ("set warning false")
GPIO.setwarnings(False)
GPIO.setup(15,GPIO.OUT)
GPIO.output(15,GPIO.HIGH)
time.sleep(1)
GPIO.output(15,GPIO.LOW)
```

generates following output

```shell
$ export LOG_LEVEL=Info
$ python examples/test.py
set mode
set warning false
2020-05-07 17:49:23,031:INFO: Set Warings as False
2020-05-07 17:49:23,031:INFO: setup channel : 15 as 0 with intial :0 and pull_up_dowm 20
2020-05-07 17:49:23,032:INFO: output channel : 15 with value : 1
2020-05-07 17:49:24,033:INFO: output channel : 15 with value : 0
```
