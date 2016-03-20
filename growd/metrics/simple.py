import requests

class SimpleMetrics(object):
    def __init__(self, url):
        self.url = url

    def send(self, temp, hum):
        r = requests.get(self.url, params={'temp': temp, 'hum': hum})
