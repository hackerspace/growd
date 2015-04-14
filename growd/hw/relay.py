class Relay(object):
    def __init__(self, device, pin, initially_on=False, connect_on_low=False):
        self.device = device
        self.pin = pin
        self.connect_on_low = connect_on_low

        self.device.gpio_setup(pin, True)
        self.switch(initially_on)

    def switch(self, switch_on):
        state = switch_on
        if self.connect_on_low:
            state = not state

        self.device.gpio_set(self.pin, state)
