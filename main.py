from machine import Pin, SoftSPI, SoftI2C, reset
from time import time

from conf import *
from mrfid import RFID
from mservo import MServo
from m_hcsr04 import HCSR
from utils import spi
from web_api import search_user
from constants import OK
from networking import Network
from credentials import WIFI_SSID, WIFI_PASSWORD

i2c = SoftI2C(scl=I2C_SCL_PIN, sda=I2C_SDA_PIN)
rfid = RFID(spi=spi, rst_pin=RFID_RST_PIN, sda_pin=RFID_SDA_PIN)
network = Network(WIFI_SSID, WIFI_PASSWORD)
network.connect_station()

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
            # query database for user information and verification
            server_response, reason = search_user(tag_code)
            """
            FIXME: Downside is that on listening to entrance gate,
              the exit gate is left unmonitored.
            """
            if server_response == OK:
                if (
                    not slot1.object_detected()
                    or not slot2.object_detected()
                    or not slot3.object_detected()
                    or not slot4.object_detected()
                ):
                    entrance_gate.open()
                    entrance_gate_open_time = time()
                else:
                    print("Unfortunately the slots are not empty!")
            else:
                print("REASON:", reason)

        if exit_detector.object_detected():
            exit_gate.open()
            exit_gate_open_time = time()

        if entrance_gate.is_open and time() - entrance_gate_open_time > 3:
            entrance_gate.close()

        if exit_gate.is_open and time() - exit_gate_open_time > 2:
            exit_gate.close()

except KeyboardInterrupt as ki:
    print("Keyboard interrupt!")
    # resetting is necessary on failure so that the SPI can be reset
    reset()
