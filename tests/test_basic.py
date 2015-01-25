import unittest
from nose.tools import *

from growd.hw.raspberry import Board
from growd.hw.relay import Relay

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
