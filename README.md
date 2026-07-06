# SX1278 MicroPython Library for Raspberry Pi Pico

[![MicroPython](https://img.shields.io/badge/MicroPython-2B2728?logo=micropython&logoColor=white)](https://micropython.org/)
[![Raspberry%20Pi%20Pico](https://img.shields.io/badge/Raspberry%20Pi-Pico%20%26%20Pico%202-C51A4A?&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/products/raspberry-pi-pico/)
[![Version](https://img.shields.io/badge/version-1.2-f883d)](https://github.com/timokoethe/SX1278/releases)
[![License](https://img.shields.io/badge/license-MIT-f883d)](https://opensource.org/license/mit)

Lightweight [MicroPython](https://micropython.org/) driver for the Ra-01 LoRa module based on the SX1278 chipset, with a setup focused on the Raspberry Pi Pico (RP2040) and Raspberry Pi Pico 2 (RP2350).

The library communicates over SPI and provides a simple API for sending and receiving LoRa packets.

## Features

- MicroPython-first API with minimal setup
- Works with Raspberry Pi Pico and Pico 2
- Blocking packet transmission with `send()`
- Interrupt-driven packet reception with `on_recv()`
- Configurable frequency, bandwidth, spreading factor, coding rate, and CRC

## Installation

Copy [`sx1278.py`](./sx1278.py) to the root of your MicroPython device, then import it in your script:

```python
from sx1278 import Lora
```

## Quick Start

Example wiring used by the snippets below:

| SX1278 / Ra-01 | Raspberry Pi Pico | Used in code |
| --- | --- | --- |
| MISO | GP0 | `MISO = 0` |
| DIO0 | GP10 | `RX = 10` |
| SCK | GP2 | `SCK = 2` |
| MOSI | GP3 | `MOSI = 3` |
| RST | GP16 | `RST = 16` |
| NSS | GP1 | `CS = 1` |
| GND | GND | power |
| 3V3 | 3V3(OUT) | power |

Set up SPI first:

```python
from machine import Pin, SPI
from sx1278 import Lora

SCK = 2
MOSI = 3
MISO = 0
CS = 1
RX = 10
RST = 16

spi = SPI(
    0,
    baudrate=10_000_000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)
spi.init()
```

Then create the LoRa instance:

```python
lr = Lora(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    rs=Pin(RST, Pin.OUT),
)
```

## Sending Data

`send()` blocks until transmission has finished or the TX timeout is reached. The default timeout is 5000 ms and can be changed with `tx_timeout_ms=` when creating `Lora`. The maximum payload length is 255 bytes.

```python
lr.send("Hello World!")
```

## Receiving Data

Register a receive handler, put the module into receive mode, and keep the script running:

```python
def handler(message):
    print(message)
    # Put the module back into receive mode after handling a packet.
    lr.recv()

lr.on_recv(handler)
lr.recv()

while True:
    pass
```

## Examples

Ready-to-run examples for the Raspberry Pi Pico are included in the [`example`](./example) directory:

- [`example/send.py`](./example/send.py)
- [`example/receive.py`](./example/receive.py)

## Important Notes

- Use a frequency that is legal for your region.
- The default frequency in [`sx1278.py`](./sx1278.py) is `433.1` MHz.
- You can override the default by passing `frequency=` when creating `Lora`, or by changing the module constant in the library.
- The default transmit power is `17` dBm. Values above `17` are clamped to `17` by the default PA_BOOST output path.

## License

This project is licensed under the MIT License. See [`LICENSE`](./LICENSE).
