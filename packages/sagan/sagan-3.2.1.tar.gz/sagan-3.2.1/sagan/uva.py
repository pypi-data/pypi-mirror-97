
from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple


UvaMeasurement = namedtuple(
    'UvaMeasurement',
    'uva'
)


class UvaSensor(I2cDevice):
    def self_test(self):
        # There is nothing to do here, only readable registers are the output data
        return True

    def configure(self, args):
        self.bus.write_byte(0x38, 0x60)

    def measure(self):
        """
        :return: UVa reading in W m^-2
        """
        # scale from sensor is 5 uW / cm^2  / encoder count.
        msb = self.bus.read_byte_data(0x39, 0x00)
        lsb = self.bus.read_byte_data(0x38, 0x00)
        result = UvaMeasurement(((msb << 8) | lsb) * 5e-2)
        packet = {
            "uva": str(result.uva)
        }
        Telemetry.update("uva", packet)
        return result

    @property
    def uva(self):
        return self.measure().uva
