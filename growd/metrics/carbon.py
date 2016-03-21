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

    def send(self, temp, hum):
        dp = dew_point(temp, hum)
        ts = int(time.time())
        msg = ("{ident}.temp {temp} {ts}\n"
               "{ident}.hum {hum} {ts}\n"
               "{ident}.dew {dp} {ts}\n"
               .format(ident=self.ident, ts=ts, temp=temp, hum=hum, dp=dp))

        # TODO: don't open new connection every time
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.sendall(msg)
        s.close()
