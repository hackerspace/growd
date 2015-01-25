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

import unittest
from nose.tools import *

from growd.hw.sht21 import _get_temperature_from_buffer, _calculate_checksum

class SHT21Test(unittest.TestCase):
    """simple sanity test"""

    def test_temperature(self):
        """Unit test to check the checksum method"""
        calc_temp = _get_temperature_from_buffer([chr(99),chr(172)])
        #floating point comparison, not pretty.
        self.failUnless(abs(calc_temp - 21.5653979492) < 0.1)

    def test_checksum(self):
        """Unit test to check the checksum method.  Uses values read"""
        self.failUnless(_calculate_checksum([chr(99),chr(172)] , 2) == 249)
        self.failUnless(_calculate_checksum([chr(99),chr(160)] , 2) == 132)
