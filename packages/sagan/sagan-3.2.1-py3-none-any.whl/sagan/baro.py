
import time
from .i2c import I2cDevice
from collections import namedtuple
from .telemetry import Telemetry

BarometerMeasurement = namedtuple(
    'BarometerMeasurement',
    'temperature pressure humidity'
)

class Barometer(I2cDevice):
    data_frame = '>HBHBH'
    parameters_frame_1 = '<HhhHhhhhhhhhB'
    parameters_frame_2 = '<hBBBBb'
    mode = 0b1  # 'Forced' mode
    pressure_oversample = 1
    temperature_oversample = 1
    humidity_oversample = 1

    temperature_parameters = [0] * 3
    pressure_parameters = [0] * 9
    humidity_parameters = [0] * 6

    """
    Interface for BME280 pressure and humidity
    """
    def read_raw_measurements(self):
        # Forced measurement mode
        if self.mode in (0b01, 0b10):
            self.configure({})
        # TODO: calculate appropriate sleep time, this is in the data sheet
        time.sleep(0.500)
        p1, p0, t1, t0, h = self.read_and_unpack(0xF7, self.data_frame)
        p = (p0 >> 4) | (p1 << 4)
        t = (t0 >> 4) | (t1 << 4)

        return t, p, h

    def apply_calibration(self, t_raw, p_raw, h_raw, t_calib=None):
        T1 = self.temperature_parameters[0]
        T2 = self.temperature_parameters[1]
        T3 = self.temperature_parameters[2]
        P1 = self.pressure_parameters[0]
        P2 = self.pressure_parameters[1]
        P3 = self.pressure_parameters[2]
        P4 = self.pressure_parameters[3]
        P5 = self.pressure_parameters[4]
        P6 = self.pressure_parameters[5]
        P7 = self.pressure_parameters[6]
        P8 = self.pressure_parameters[7]
        P9 = self.pressure_parameters[8]
        H1 = self.humidity_parameters[0]
        H2 = self.humidity_parameters[1]
        H3 = self.humidity_parameters[2]
        H4 = self.humidity_parameters[3]
        H5 = self.humidity_parameters[4]
        H6 = self.humidity_parameters[5]

        var1 = (t_raw / 16384.0 - T1 / 1024.0) * T2
        var2 = ((t_raw / 131072.0 - T1 / 8192.0) * (t_raw / 131072.0 - T1 / 8192.0)) * T3
        t_fine = int(var1 + var2)
        t = (var1 + var2) / 5120.0

        if t_calib is not None:
            t_fine = t_calib

        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * P6 / 32768.0
        var2 = var2 + var1 * P5 * 2.0
        var2 = var2 / 4.0 + P4 * 65536.0
        var1 = (P3 * var1 * var1 / 524288.0 + P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * P1
        if var1 == 0:
            p = 0
        else:
            p = 1048576.0 - p_raw
            p = ((p - var2 / 4096.0) * 6250.0) / var1
            var1 = P9 * p * p / 2147483648.0
            var2 = p * P8 / 32768.0
            p = p + (var1 + var2 + P7) / 16.0
        p = p

        h = t_fine - 76800.0
        h = (h_raw - (H4 * 64.0 + H5 / 16384.8 * h)) * (
            H2 / 65536.0 * (1.0 + H6 / 67108864.0 * h * (
                1.0 + H3 / 67108864.0 * h)))
        h = h * (1.0 - H1 * h / 524288.0)
        if h > 100:
            h = 100
        elif h < 0:
            h = 0

        packet = {
            "t": t,
            "p": p,
            "h": h
        }

        Telemetry.update("bar", packet)
        return t, p, h

    def measure(self):
        """
        :return: tuple of: temperature (C), pressure (Pa), humidity (% relative humidity)
        """
        return BarometerMeasurement(*self.apply_calibration(*self.read_raw_measurements()))

    def self_test(self):
        id, = self.read_and_unpack(0xD0, 'B')
        return id == 0x60

    def configure(self, args):
        self.read_parameters()
        ctrl_meas = (self.temperature_oversample << 5) | (self.pressure_oversample << 2) | self.mode
        ctrl_hum = self.humidity_oversample & 0b00000111
        self.pack_and_write(0xF2, 'B', ctrl_hum)
        self.pack_and_write(0xF4, 'B', ctrl_meas)

    def read_parameters(self):
        frame_1 = self.read_and_unpack(0x88, self.parameters_frame_1)
        self.temperature_parameters = frame_1[0:3]
        self.pressure_parameters = frame_1[3:12]

        frame_2 = self.read_and_unpack(0xE1, self.parameters_frame_2)
        self.humidity_parameters[0] = frame_1[12]
        self.humidity_parameters[1:3] = frame_2[0:2]
        self.humidity_parameters[3] = (frame_2[2] << 4) | (frame_2[3] & 0x0F)
        self.humidity_parameters[4] = (frame_2[4] << 4) | (frame_2[3] & 0xF0)
        self.humidity_parameters[5] = frame_2[5]

    @property
    def temperature(self):
        return self.measure().temperature

    @property
    def pressure(self):
        return self.measure().pressure

    @property
    def humidity(self):
        return self.measure().humidity
