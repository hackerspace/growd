import sys

try:
    import RPi.GPIO as GPIO
except ImportError:
    sys.stderr.write('RPi.GPIO not found!')
except RuntimeError:
    sys.stderr.write('Error importing RPi.GPIO! You probably need to run this as root.')

class Board(object):
    def __init__(self):
        pass

    def cleanup(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, ty, value, traceback):
        self.cleanup()

class Raspberry(Board):
    def __init__(self):
        super(Raspberry, self).__init__()

        if not 'GPIO' in globals():
            raise RuntimeError('GPIO module error');

        GPIO.setmode(GPIO.BOARD)

    def gpio_setup(self, num, is_output):
        GPIO.setup(num, GPIO.OUT if is_output else GPIO.IN)

    def gpio_set(self, num, value):
        GPIO.output(num, value)

    def cleanup(self):
        GPIO.cleanup()
