#
# This file is based on file written by Richard Jaques and published at
# https://github.com/jaques/sht21_python
# Text of the file's license follows:
#
# The MIT License (MIT)
#
# Copyright (c) 2013 Richard Jaques
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time

class SHT21(object):
    """Class to read temperature and humidity from SHT21, much of class was
    derived from: #http://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity/Sensirion_Humidity_SHT21_Datasheet_V3.pdf
    and Martin Steppuhn's code from http://www.emsystech.de/raspi-sht21"""

    #control constants
    _I2C_ADDRESS = 0x40
    _SOFTRESET = 0xFE
    _TRIGGER_TEMPERATURE_NO_HOLD = 0xF3
    _TRIGGER_HUMIDITY_NO_HOLD = 0xF5

    def __init__(self, i2c):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded)."""
        self.i2c = i2c
        self.i2c.write(chr(self._SOFTRESET))
        time.sleep(0.050)

    def read_temperature(self):
        """Reads the temperature from the sensor.  Not that this call blocks
        for 250ms to allow the sensor to return the data"""
        self.i2c.write(chr(self._TRIGGER_TEMPERATURE_NO_HOLD))
        time.sleep(0.250)
        data = self.i2c.read(3)
        if _calculate_checksum(data,2) == ord(data[2]):
            return _get_temperature_from_buffer(data)

    def read_humidity(self):
        """Reads the humidity from the sensor.  Not that this call blocks
        for 250ms to allow the sensor to return the data"""
        self.i2c.write(chr(self._TRIGGER_HUMIDITY_NO_HOLD))
        time.sleep(0.250)
        data = self.i2c.read(3)
        if _calculate_checksum(data,2) == ord(data[2]):
            return _get_humidity_from_buffer(data)


def _calculate_checksum(data, nbrOfBytes):
    """5.7 CRC Checksum using teh polynomial given in the datasheet"""
    # CRC
    POLYNOMIAL = 0x131 # //P(x)=x^8+x^5+x^4+1 = 100110001
    crc = 0
    #calculates 8-Bit checksum with given polynomial
    for byteCtr in range(nbrOfBytes):
        crc ^= (ord(data[byteCtr]))
        for bit in range(8,0,-1):
            if (crc & 0x80):
                crc = (crc << 1) ^ POLYNOMIAL
            else:
                crc = (crc << 1)
    return crc


def _get_temperature_from_buffer(data):
    """This function reads the first two bytes of data and
    returns the temperature in C by using the following function:
    T = =46.82 + (172.72 * (ST/2^16))
    where ST is the value from the sensor
    """
    unadjusted = (ord(data[0]) << 8) + ord(data[1])
    unadjusted *= 175.72
    unadjusted /= 1 << 16 # divide by 2^16
    unadjusted -= 46.85
    return unadjusted


def _get_humidity_from_buffer(data):
    """This function reads the first two bytes of data and returns
    the relative humidity in percent by using the following function:
    RH = -6 + (125 * (SRH / 2 ^16))
    where SRH is the value read from the sensor
    """
    unadjusted = (ord(data[0]) << 8) + ord(data[1])
    unadjusted *= 125.0
    unadjusted /= 1 << 16 # divide by 2^16
    unadjusted -= 6
    return unadjusted
