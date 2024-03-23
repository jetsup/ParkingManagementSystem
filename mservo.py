from machine import I2C
from servo import Servos


class MServo:

    def __init__(
        self,
        i2c: I2C,
        channel: int,
        offset_angle: int = 0,
        address=0x40,
        freq=50,
        min_us=600,
        max_us=2400,
        degrees=180,
    ):
        self.servo = Servos(
            i2c=i2c,
            address=address,
            freq=freq,
            min_us=min_us,
            max_us=max_us,
            degrees=degrees,
        )
        self.channel = channel
        self.offset = offset_angle
        self.is_open = False
        # close the gate by default
        self.close()

    def open(self):
        self.is_open = True
        self.servo.position(self.channel, 90 + self.offset)

    def close(self):
        self.is_open = False
        self.servo.position(self.channel, 0 + self.offset)
