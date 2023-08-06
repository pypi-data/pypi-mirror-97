from sagan import temperature
from nose.tools import eq_


def test_temperature_parse():
    eq_(temperature._parse_temp_bytes(0b01111111, 0), 127.0)
    eq_(temperature._parse_temp_bytes(0b01111110, 0b11100000),  126.875)
    eq_(temperature._parse_temp_bytes(0b01111110, 0b00100000),  126.125)
    eq_(temperature._parse_temp_bytes(0b01111101, 0b00000000),  125.000)
    eq_(temperature._parse_temp_bytes(0b00011001, 0b00000000),   25.000)
    eq_(temperature._parse_temp_bytes(0b00000000, 0b00100000),    0.125)
    eq_(temperature._parse_temp_bytes(0b00000000, 0b00000000),    0.000)
    eq_(temperature._parse_temp_bytes(0b11111111, 0b11100000),   -0.125)
    eq_(temperature._parse_temp_bytes(0b11100111, 0b00000000),  -25.000)
    eq_(temperature._parse_temp_bytes(0b11001001, 0b00100000),  -54.875)
    eq_(temperature._parse_temp_bytes(0b11001001, 0b00000000),  -55.000)
