from abc import abstractmethod

import struct
import smbus


class I2cDevice:
    """
    A light wrapper on top of smbus for convenience.
    """
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read(self, cmd, length):
        return self.bus.read_i2c_block_data(self.address, cmd, length)

    def write(self, cmd, values):
        return self.bus.write_i2c_block_data(self.address, cmd, values)

    def read_and_unpack(self, cmd, fmt):
        s = struct.Struct(fmt)
        b = bytes(self.read(cmd, s.size))
        return s.unpack(b)

    def pack_and_write(self, cmd, fmt, values):
        s = struct.Struct(fmt)
        b = s.pack(values)
        return self.write(cmd, [c for c in b])

    @abstractmethod
    def configure(self, args):
        pass

    @abstractmethod
    def self_test(self):
        pass

    def __repr__(self):
        return "{}(bus={}, address={})".format(type(self).__name__, self.bus, self.address)
