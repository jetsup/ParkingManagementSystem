from machine import Pin, SPI, SoftI2C, reset
from conf import *
from time import time

from mrfid import RFID
from mservo import MServo

spi = SPI(
    2,
    baudrate=SPI_BAUDRATE,
    polarity=0,
    phase=0,
    sck=Pin(SPI_SCK_PIN, Pin.OUT),
    mosi=Pin(SPI_MOSI_PIN, Pin.OUT),
    miso=Pin(SPI_MISO_PIN, Pin.OUT),
)

i2c = SoftI2C(scl=I2C_SCL_PIN, sda=I2C_SDA_PIN)

rfid = RFID(spi, RFID_RST_PIN, RFID_SDA_PIN)
entrance_gate = MServo(i2c, channel=14, offset_angle=30)
exit_gate = MServo(i2c, channel=14, offset_angle=30)

try:
    while True:
        tag_code = rfid.read()
        if tag_code:
            print(f"TAG: {tag_code}")

except KeyboardInterrupt as ki:
    print("Keyboard interrupt!")
    # resetting is necessary on failure so that the SPI can be reset
    reset()
