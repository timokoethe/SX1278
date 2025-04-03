# MicroPython library for the SX1278 
[![MicroPython](https://img.shields.io/badge/MicroPython-2B2728?style=for-the-badge&logo=micropython&logoColor=0f0)](https://micropython.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-mint)](https://opensource.org/license/mit)

This repository provides a lightweight [MicroPython](https://micropython.org/) library for the Ra-01 LoRa module, based on the SX1278 chipset, designed for use with the Raspberry Pi Pico (RP2040) or the Raspberry Pi Pico 2 (RP2350). The library supports communication via SPI.
  
## Installation
Copy the file ```sx1278.py``` to the root directory of your microcontroller. 
Then, import the module using ```from sx1278 import Lora```.
Ensure you are using the correct frequency for your region. 
You can adjust this at the top of the library file by modifying the relevant variable.

## Setup
First connect and setup SPI for the LoRa module:
```python
# Setup SPI
spi = SPI(0, baudrate=10000000,
          sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
          mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
          miso=Pin(MISO, Pin.IN, Pin.PULL_UP))
spi.init()
```

Next, setup the module. Make sure to connect cs, rx and rst pins correctly.
```python
# Setup the lora module
lr = Lora(spi,
            cs=Pin(CS, Pin.OUT),
            rx=Pin(RX, Pin.IN),
            rs=Pin(RS, Pin.OUT))
```

## Sending Data
This method blocks until the sending is completed. The maximum package length is 255 bytes.
```python
lr.send('Hello World!')
```

## Receiving Data
The module operates in receiving mode to receive data. When a message is received, a handler is executed. 
To keep the program running, use a loop where any necessary break conditions can be implemented.
```python
# Handles incoming messages
def handler(message):
    print(message)
    # Puts module back in receiving mode
    lr.recv()

# Sets handler
lr.on_recv(handler)
# Puts module in receiving mode
lr.recv()

# Prevents the program from stopping
while True:
    pass
```


