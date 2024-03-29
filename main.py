from machine import Pin, SoftSPI, SoftI2C, reset
from conf import *
from time import time

from mrfid import RFID
from mservo import MServo
from m_hcsr04 import HCSR

spi = SoftSPI(
    baudrate=SPI_BAUDRATE,
    polarity=0,
    phase=0,
    sck=Pin(SPI_SCK_PIN, Pin.OUT),
    mosi=Pin(SPI_MOSI_PIN, Pin.OUT),
    miso=Pin(SPI_MISO_PIN, Pin.OUT),
)

i2c = SoftI2C(scl=I2C_SCL_PIN, sda=I2C_SDA_PIN)

rfid = RFID(spi=spi, rst_pin=RFID_RST_PIN, sda_pin=RFID_SDA_PIN)

print("Creating Gates")
# tune the offset angles to  match the physical position of the servo
entrance_gate = MServo(i2c, channel=ENTRANCE_GATE_CHANNEL, offset_angle=30)
exit_gate = MServo(i2c, channel=EXIT_GATE_CHANNEL, offset_angle=30)
print("Created Gates")

print("Creating SLots")
slot1 = HCSR(HCSR04_TRIGGER_PIN_SLOT_1, HCSR04_ECHO_PIN_SLOT_1)
slot2 = HCSR(HCSR04_TRIGGER_PIN_SLOT_2, HCSR04_ECHO_PIN_SLOT_2)
slot3 = HCSR(HCSR04_TRIGGER_PIN_SLOT_3, HCSR04_ECHO_PIN_SLOT_3)
slot4 = HCSR(HCSR04_TRIGGER_PIN_SLOT_4, HCSR04_ECHO_PIN_SLOT_4)
exit_detector = HCSR(HCSR04_TRIGGER_PIN_SLOT_EXIT, HCSR04_ECHO_PIN_SLOT_EXIT)
print("Created SLots")

close_prev = 0
opened = False

try:
    while True:
        print(
            "1: ",
            slot1.distance_cm(),
            " 2: ",
            slot2.distance_cm(),
            " 3: ",
            slot3.distance_cm(),
            " 4: ",
            slot4.distance_cm(),
            " exit: ",
            exit_detector.distance_cm(),
        )
        tag_code = rfid.read_data()
        if tag_code:
            print(f"TAG: {tag_code}")
        if time() - close_prev >= 2:
            if opened:
                entrance_gate.close()
                exit_gate.close()
                opened = False
                close_prev = time()
            else:
                entrance_gate.open()
                exit_gate.open()
                opened = True
                close_prev = time()

except KeyboardInterrupt as ki:
    print("Keyboard interrupt!")
    # resetting is necessary on failure so that the SPI can be reset
    reset()
