import time
import logging
from collections import namedtuple

# Atlas Scientific EZO pH circuit
# https://www.atlas-scientific.com/product_pages/circuits/ezo_ph.html
# This file is based on example code provided with the device.

# The device has to be switched into I2C mode first by shorting TX to PGND and
# then powering the device on (the LED should turn blue).

logger = logging.getLogger('ezo_ph')

class EzoPH(object):

    _DEFAULT_ADDRESS = 0x63
    _LONG_WAIT_TIME = 1.0
    _SHORT_WAIT_TIME = 0.5 # manual: 0.3
    _CAL_WAIT_TIME = 2.0 # manual: 1.6

    Slope = namedtuple('Slope', ['acid', 'base'])
    Info = namedtuple('Info', ['dev_type', 'fw_version'])
    Status = namedtuple('Status', ['restart_reason', 'vcc'])

    class Error(Exception): pass
    class ReadError(Error):
        def __init__(self, error_code):
            self.args = (error_code,)
            reason = {
                1: "success?",
                2: "request failed",
                254: "request pending, try again later",
                255: "no request, no data"
            }.get(error_code, "(unknown error code)")
            self.message = "I2C read error {0}: {1}".format(error_code, reason)

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address

    def _write(self, string):
        self.i2c.write(string + "\x00")

    def _read(self, n=31):
        res = self.i2c.read(n)
        response = filter(lambda x: x != '\x00', res)
        error_n = ord(response[0])

        if(error_n == 1): # success
            # change MSB to 0 for all received characters except the first and get a list of characters 
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
            return ''.join(char_list)
        else:
            error_n = ord(response[0])
            raise EzoPH.ReadError(error_n)

    def query(self, command, parse_prefix=None, parse_args=0, read_response=True, wait=_SHORT_WAIT_TIME):
        self.i2c.set_address(self.address)

        command = command.upper()
        logger.debug("> " + command)
        self._write(command)
        time.sleep(wait)

        if not read_response: #sleep mode, factory reset
            return None

        response = self._read()
        logger.debug("< " + response)

        if parse_prefix:
            parts = response.split(',')

            if (parts[0].upper() != ('?' + parse_prefix).upper()
                    or len(parts) != parse_args + 1):
                raise EzoPH.Error("Response not understood: " + response)

            return parts[1:]

        return response

    def read_ph(self):
        response = self.query("R", wait=self._LONG_WAIT_TIME)
        return float(response)

    def read_slope(self):
        response = self.query("SLOPE,?", parse_prefix="SLOPE", parse_args=2)
        return self.Slope(float(response[0]), float(response[1]))

    def read_info(self):
        response = self.query("I", parse_prefix="I", parse_args=2)
        return self.Info(response[0], response[1])

    def _parse_status(self, response):
        restart_code = response[0]
        reason = {
                'P': 'power on reset',
                'S': 'software reset',
                'B': 'brown out reset',
                'W': 'watchdog reset',
                'U': 'unknown',
            }.get(restart_code, "Unknown reason: {0}".format(restart_code))
        return self.Status(reason, float(response[1]))

    def read_status(self):
        response = self.query("STATUS", parse_prefix="STATUS", parse_args=2)
        return self._parse_status(response)

    def read_calibration_status(self):
        response = self.query("CAL,?", parse_prefix="CAL", parse_args=1)
        return int(response[0])

    def read_temp_compensation(self):
        response = self.query("T,?", parse_prefix="T", parse_args=1)
        return float(response[0])

    def set_temp_compensation(self, temp=None):
        if not temp:
            temp = 25.0

        cmd = "T,{0:.2f}".format(temp)
        self.query(cmd)

    def set_led(self, state):
        cmd = "L,{0}".format("1" if state else "0")
        self.query(cmd)

    def sleep(self):
        self.query("SLEEP", read_response=False)

    def factory_reset(self):
        self.query("FACTORY", read_response=False, wait=4)

    def calibrate_mid(self, value=7.00):
        self.query("CAL,MID,{0:.2f}".format(value), wait=self._CAL_WAIT_TIME)

    def calibrate_low(self, value=4.00):
        self.query("CAL,LOW,{0:.2f}".format(value), wait=self._CAL_WAIT_TIME)

    def calibrate_high(self, value=10.00):
        self.query("CAL,HIGH,{0:.2f}".format(value), wait=self._CAL_WAIT_TIME)

if __name__ == '__main__':
    from growd.hw.raspberry import Raspberry

    logging.basicConfig(level=logging.DEBUG)

    with Raspberry() as rpi:
        rpi.i2c_setup()
        ph = EzoPH(rpi.i2c[1])

        import IPython
        IPython.embed()
