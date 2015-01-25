class Relay(object):
    def __init__(self, device, pin, initially_on=False):
        self.device = device
        self.pin = pin

        self.device.gpio_setup(pin, True)
        self.switch(initially_on)

    def switch(self, switch_on):
        self.device.gpio_set(self.pin, switch_on)
