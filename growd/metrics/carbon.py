import time
import socket

from growd.utils import dew_point

class CarbonMetrics(object):
    def __init__(self, host, ident=None, port=2003):
        self.host = host
        self.port = port
        self.ident = "growd"
        if ident:
            self.ident += ("." + ident)

    def send(self, sensors, relays):
        sensors['dew'] = dew_point(sensors['temp'], sensors['hum'])
        ts = int(time.time())
        msg = ""

        for sensor, val in sensors.items():
            msg += ("{ident}.{sensor} {val} {ts}\n"
                    .format(ident=self.ident, sensor=sensor, val=val, ts=ts))

        for relay, state in relays.items():
            val = 1 if state else 0
            msg += ("{ident}.relay.{relay} {val} {ts}\n"
                    .format(ident=self.ident, relay=relay, val=val, ts=ts))

        # TODO: don't open new connection every time
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.sendall(msg)
        s.close()
