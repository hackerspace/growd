class MCP23009(object):
    """
    Microchip MCP23009 8-Bit I/O Expander with Open-Drain Outputs
    Datasheet: http://ww1.microchip.com/downloads/en/DeviceDoc/22121b.pdf
    """
    _IODIR = 0x00
    _GPIO  = 0x09

    def __init__(self, i2c, i2c_address=None):
        self.i2c = i2c
        self.i2c_address = i2c_address or 0x20

    def gpio_setup(self, num, is_output):
        self.i2c.set_address(self.i2c_address)
        iodir = self.i2c.read_register(self._IODIR)

        mask = 1 << num
        if is_output:
            self.i2c.write_register(self._IODIR, iodir & ~mask)
        else:
            self.i2c.write_register(self._IODIR, iodir | mask)

    def gpio_set(self, num, value):
        self.i2c.set_address(self.i2c_address)
        gpio = self.i2c.read_register(self._GPIO)

        mask = 1 << num
        if value:
            self.i2c.write_register(self._GPIO, gpio & ~mask)
        else:
            self.i2c.write_register(self._GPIO, gpio | mask)
