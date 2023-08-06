from operator import add
from functools import reduce

from nose.tools import assert_almost_equal

from sagan.rgb_ir import _parse_rgb_ir_bytes


def encode_24bit_channel(value):
    return [value & 0xFFFF, value >> 16]


def encode_4_channel_bytes(values):
    return reduce(add, (encode_24bit_channel(channel) for channel in values), [])


def test_rgb_ir_parse():
    for i in range(10, 2 ** 24, 400000):
        inputs = (i * 0.1, i * 0.2, i * 0.3, i * 0.4)
        inputs = [int(x) for x in inputs]
        colour_bytes = encode_4_channel_bytes(inputs)
        total = sum(inputs)
        required = [x / total for x in inputs]
        actual = _parse_rgb_ir_bytes(colour_bytes)
        assert_almost_equal(actual[0], required[3])
        assert_almost_equal(actual[1], required[1])
        assert_almost_equal(actual[2], required[2])
        assert_almost_equal(actual[3], required[0])
