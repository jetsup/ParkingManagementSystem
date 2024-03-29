from machine import Pin, time_pulse_us
from time import sleep_ms
from hcsr04 import HCSR04

class HCSR(HCSR04):
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500 * 2 * 30):
        super().__init__(trigger_pin, echo_pin, echo_timeout_us)
    pass