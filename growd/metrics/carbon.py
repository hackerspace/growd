import time
import socket

class CarbonMetrics(object):
    def __init__(self, host, ident=None, port=2003):
        self.host = host
        self.port = port
        self.ident = "growd"
        if ident:
            self.ident += ("." + ident)

    def send(self, sensors):
        ts = int(time.time())
        msg = ""

        for sensor, val in sensors.items():
            msg += ("{ident}.{sensor} {val} {ts}\n"
                    .format(ident=self.ident, sensor=sensor, val=val, ts=ts))

        # TODO: don't open new connection every time
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.sendall(msg)
        s.close()
