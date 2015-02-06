import unittest
import StringIO

from nose.tools import *

from growd.hw.watchdog import Watchdog

class MockDog(StringIO.StringIO):
    def __init__(self):
        StringIO.StringIO.__init__(self)
        self.was_closed = False

    def close(self):
        self.was_closed = True

    def really_close(self):
        StringIO.StringIO.close(self)

class TestWatchdog(unittest.TestCase):
    def setUp(self):
        self.mock = MockDog()

    def tearDown(self):
        self.mock.really_close()

    def test_watchdog(self):
        assert_equal(self.mock.getvalue(), "")

        w = Watchdog(fh=self.mock)
        w.keepalive()

        nwritten = len(self.mock.getvalue())
        assert_greater(nwritten, 0)

        w.keepalive()

        nwritten2 = len(self.mock.getvalue())
        assert_greater(nwritten2, nwritten)

        w.close()

        written3 = self.mock.getvalue()
        assert_greater(len(written3), nwritten2)
        assert_equal(written3[-1], 'V')
        assert_true(self.mock.was_closed)

    def test_context(self):
        assert_equal(self.mock.getvalue(), "")

        with Watchdog(fh=self.mock) as w:
            w.keepalive()

            nwritten = len(self.mock.getvalue())
            assert_greater(nwritten, 0)

            w.keepalive()

            nwritten2 = len(self.mock.getvalue())
            assert_greater(nwritten2, nwritten)

        written3 = self.mock.getvalue()

        assert_greater(len(written3), nwritten2)
        assert_equal(written3[-1], 'V')
        assert_true(self.mock.was_closed)

    def test_explicit(self):
        assert_equal(self.mock.getvalue(), "")

        try:
            with Watchdog(fh=self.mock, needs_explicit_close=True) as w:
                w.keepalive()
                raise StopIteration
        except StopIteration:
            pass

        written = self.mock.getvalue()
        assert_not_equal(written[-1], 'V')
        assert_false(self.mock.was_closed)
