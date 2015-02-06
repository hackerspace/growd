import os
import logging

class Watchdog(object):
    def __init__(self, device='/dev/watchdog', needs_explicit_close=False, fh=None):
        self.logger = logging.getLogger('watchdog')
        self.needs_explicit_close = needs_explicit_close

        if fh:
            self.fh = fh
        else:
            self.fh = open(device, 'w')

        self.logger.info('Watchdog enabled')

    def _synced_write(self, s):
        self.fh.write(s)
        self.fh.flush()

    def keepalive(self):
        self._synced_write('!')

    def close(self):
        self._synced_write('V') # magic close character
        self.fh.close()

        self.logger.info('Watchdog disabled')

    def __enter__(self):
        return self

    # TODO: don't close on exceptions? what about KeyboardInterrupt?
    def __exit__(self, ty, value, traceback):
        if not self.needs_explicit_close:
            self.close()
        else:
            exc_info = (ty, value, traceback) if ty else False
            self.logger.error('Exited watchdog context with watchdog still enabled', exc_info=exc_info)
