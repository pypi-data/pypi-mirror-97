
from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple


RgbIrMeasurement = namedtuple(
    'RgbIrMeasurement',
    'red green blue ir'
)


def _parse_rgb_ir_bytes(colour_data):
    measurement = tuple((colour_data[2 * i + 1] << 16) | colour_data[2 * i] for i in range(4))
    total = sum(measurement)
    if total == 0:
        return 0, 0, 0, 0
    measurement = tuple(x / total for x in measurement)

    packet = {
        "r": str(measurement[3]),
        "g": str(measurement[1]),
        "b": str(measurement[2]),
        "ir": str(measurement[0])
    }

    Telemetry.update("rgb", packet)
    return measurement[3], measurement[1], measurement[2], measurement[0]


class RgbIrSensor(I2cDevice):
    def self_test(self):
        id = self.read(0x06, 1)[0]
        return id == 0xB2

    def configure(self, args):
        # set light sensor enabled, colour sensing mode.
        self.pack_and_write(0x00, 'B', 0b00000110)
        super().configure(args)

    def measure(self):
        """
        :return: R, G, B and IR Channel readings and a fraction of the total.
        """
        colour_data = self.read_and_unpack(0x0A, '<BHBHBHBH')
        return RgbIrMeasurement(*_parse_rgb_ir_bytes(colour_data))

    @property
    def red(self):
        return self.measure()[0]

    @property
    def green(self):
        return self.measure()[1]

    @property
    def blue(self):
        return self.measure()[2]

    @property
    def ir(self):
        return self.measure()[3]
