import requests

class SimpleMetrics(object):
    def __init__(self, url):
        self.url = url

    def send(self, sensors, relays):
        r = requests.get(self.url, params=sensors)
