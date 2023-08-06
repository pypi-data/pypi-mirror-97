from math import floor

from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple
import datetime

RtcTimeMeasurement = namedtuple('RtcTimeTuple', 'year month week_day day hour minute second hundredths_of_seconds')


def _parse_rtc_bytes(time_regs):
    hundredths_of_seconds = ((time_regs[0] & 0xF0) >> 4) * 10 + (time_regs[0] & 0x0F)
    seconds = ((time_regs[1] & 0x70) >> 4) * 10 + (time_regs[1] & 0x0F)
    minutes = ((time_regs[2] & 0x70) >> 4) * 10 + (time_regs[2] & 0x0F)
    hours = ((time_regs[3] & 0x30) >> 4) * 10 + (time_regs[3] & 0x0F)
    days = ((time_regs[4] & 0x30) >> 4) * 10 + (time_regs[4] & 0x0F)
    week_day = time_regs[5] & 0x07
    month = ((time_regs[6] & 0x10) >> 4) * 10 + (time_regs[6] & 0x0F)
    year = ((time_regs[7] & 0xF0) >> 4) * 10 + (time_regs[7] & 0x0F)
    return RtcTimeMeasurement(year, month, week_day, days, hours, minutes, seconds, hundredths_of_seconds)


def pack_bcd_lt_100(i):
    i, i_0 = divmod(i, 10)
    i_1 = i % 10
    return i_1 << 4 | i_0


def _pack_rtc_bytes(t: 'datetime.datetime'):
    time_regs = [0] * 8
    hectosecond = floor(t.microsecond / 10000)
    time_regs[0] = pack_bcd_lt_100(hectosecond)
    time_regs[1] = pack_bcd_lt_100(t.second)
    time_regs[2] = pack_bcd_lt_100(t.minute)
    time_regs[3] = pack_bcd_lt_100(t.hour)
    time_regs[4] = pack_bcd_lt_100(t.day)
    time_regs[5] = pack_bcd_lt_100(t.weekday())
    time_regs[6] = pack_bcd_lt_100(t.month)
    time_regs[7] = pack_bcd_lt_100(t.year)

    return time_regs


class RealTimeClock(I2cDevice):
    def self_test(self):
        return True

    def configure(self, kwargs):
        self.write(0x28, [0x80])
        self.write(0x25, [0x20])

        time = kwargs.get('time')
        if time is not None:
            self.set_time(time)

    def set_time(self, time):
        self.write(0x0, _pack_rtc_bytes(time))

    def measure(self):
        """
        :return: Current real time clock values
        :rtype: RtcTimeTuple
        """
        time_regs = self.read_and_unpack(0x00, 'B' * 8)
        result = _parse_rtc_bytes(time_regs)

        packet = {
            "hs": str(result.hundredths_of_seconds),
            "s": str(result.second),
            "m": str(result.minute),
            "h":  str(result.hour),
            "d": str(result.day),
            "wd": str(result.week_day),
            "mo": str(result.month),
            "y": str(result.year),
        }

        Telemetry.update("rtc", packet)

        return result
