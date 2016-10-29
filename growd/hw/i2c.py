import fcntl
import logging

logger = logging.getLogger('i2c')

class I2CBus(object):
    def __init__(self, dev_i2c):
        self.dev = open(dev_i2c, 'r+', buffering=0)

    # FIXME: is this address per-FD? in that case we should open new FD for each
    # address (= I2C slave)
    def set_address(self, addr):
        #from: linux/i2c-dev.h
        I2C_SLAVE = 0x0703
        I2C_SLAVE_FORCE = 0x0706

        fcntl.ioctl(self.dev, I2C_SLAVE, addr)

    def read(self, n):
        return self.dev.read(n)

    def write(self, data):
        self.dev.write(data)

    def read_register(self, reg):
        self.write(chr(reg))
        return ord(self.read(1))

    def write_register(self, reg, val):
        self.write(chr(reg) + chr(val))

    def cleanup(self):
        self.dev.close()
        self.dev = None
