
from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple


TemperatureMeasurement = namedtuple(
    'TemperatureMeasurement',
    'temperature'
)

def _parse_temp_bytes(hi, lo):
    value = ((hi << 8) | lo) >> 5
    if hi & (1 << 7):
        value = - ((~value & ((1 << 11) - 1)) + 1)
    value *= 0.125
    return value


class TemperatureSensor(I2cDevice):
    """
    Interface for LM75B.
    """
    def measure(self):
        """
        :return: Temperature reading in C
        """
        temp = self.read(0, 2)
        result = TemperatureMeasurement(_parse_temp_bytes(temp[0], temp[1]))
        packet = {
            "temperature": str(result.temperature)
        }
        Telemetry.update("bot" if self.address == 0x48 else "top", packet)
        return result

    def self_test(self):
        # not sure what self test to do.
        # read and write a register?
        return True

    @property
    def temperature(self):
        return self.measure().temperature

