from sx1278 import Lora
from machine import Pin, SPI
from time import sleep

# Setup Pins
SCK  = 2
MOSI = 3
MISO = 0
CS   = 1
RX   = 10
RS   = 16

# Setup SPI
spi = SPI(0, baudrate=10000000,
          sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
          mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
          miso=Pin(MISO, Pin.IN, Pin.PULL_UP))
spi.init()

# Setup LoRa
lr = Lora(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    rs=Pin(RS, Pin.OUT))

# Receive handler
def onReceive(x):
    print(x)
    # Put module back in receiving mode
    lr.recv()

# Set handler
lr.on_recv(onReceive)
# Put module in receiving mode
lr.recv()

while True:
    pass
