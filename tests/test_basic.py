import unittest

from nose.tools import *

from growd.hw.raspberry import Board
from growd.hw.relay import Relay
from growd.utils import dew_point

class MockBerry(Board):
    def __init__(self):
        self.pins = {}

    def gpio_setup(self, num, is_output):
        assert_equal(is_output, True) # don't need inputs for now
        self.pins[num] = None

    def gpio_set(self, num, value):
        assert_is_instance(num, int)
        assert_is_instance(value, bool)
        assert_in(num, self.pins, 'Pin not set up')
        self.pins[num] = value

class TestPi(unittest.TestCase):
    def setUp(self):
        self.pi = MockBerry()

    def tearDown(self):
        self.pi.cleanup()

    def test_relay(self):
        relay = Relay(self.pi, 5)
        assert_equal(self.pi.pins[5], False)
        relay.switch(True)
        assert_equal(self.pi.pins[5], True)
        relay.switch(True)
        assert_equal(self.pi.pins[5], True)
        relay.switch(False)
        assert_equal(self.pi.pins[5], False)

class TestUtils(unittest.TestCase):
    def test_dew_point(self):
        assert_almost_equal(dew_point(42.0, 100.0), 42.0)
        assert_almost_equal(dew_point(12.0, 100.0), 12.0)
        assert_almost_equal(dew_point(25.0, 40.0), 10.45726068)
        assert_almost_equal(dew_point(28.0, 35.0), 11.1082555)
