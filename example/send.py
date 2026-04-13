from sx1278 import Lora
from machine import Pin, SPI
from time import sleep

SCK  = 2
MOSI = 3
MISO = 0
CS   = 1
RX   = 10
RST  = 16

MESSAGE = "Hello World!"

spi = SPI(
    0, 
    baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP))
spi.init()

lr = Lora(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    rs=Pin(RST, Pin.OUT))

while True:
    lr.send(MESSAGE)
    print('Sent:', MESSAGE)
    sleep(1)
