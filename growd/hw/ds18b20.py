import os.path

# XXX: $ echo ds2482 0x18 > /sys/bus/i2c/devices/i2c-0/new_device
# this should be done by device tree overlay probably

class DS18B20(object):
    class Error(Exception): pass

    def __init__(self, serial=None):
        self.syspath = "/sys/bus/w1/devices/w1_bus_master1"
        self.family = 28
        self.serial = serial

        if not self.serial:
            self._pick_first_device()

    def _pick_first_device(self):
        slavesfile = os.path.join(self.syspath, 'w1_master_slaves')
        with open(slavesfile, 'r') as f:
            all_devs = f.read().splitlines()

        for dev in all_devs:
            if dev.startswith(str(self.family)+'-'):
                self.serial = dev
                return dev
        else:
            raise DS18B20.Error("No suitable device (family %s) found in %s" % self.family, slavesfile)

    def read_temperature(self):
        datafile = os.path.join(self.syspath, self.serial, 'w1_slave')
        with open(datafile, 'r') as f:
            lines = f.read().splitlines()

        if lines[0].endswith('YES'):
            tstr = lines[1].split('=')[1]
            return float(tstr) / 1000
        elif lines[0].endswith('NO'):
            raise DS18B20.Error("CRC failed")
        else:
            raise DS18B20.Error("Error reading data: %s" % lines)

    def read_sensor(self):
        return {'temp': self.read_temperature()}
