from nose.tools import *

from growd.hardware import Relay, Board

class MockBerry(Board):
    def __init__(self):
        self.pins = {}

    def gpio_setup(self, num, is_output):
        assert_equal(is_output, True) # don't need inputs for now

    def gpio_set(self, num, value):
        assert_is_instance(num, int)
        assert_is_instance(value, bool)
        self.pins[num] = value

def setup():
    pass

def teardown():
    pass

def test_sanity():
    assert(True)

def test_relay():
    with MockBerry() as pi:
        relay = Relay(pi, 5)
        assert_equal(pi.pins[5], False)
        relay.switch(True)
        assert_equal(pi.pins[5], True)
