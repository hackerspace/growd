from growd.metrics.simple import SimpleMetrics
from growd.metrics.carbon import CarbonMetrics

class MetricsSender(object):
    def __init__(self, config):
        self.metrics_receivers = []

        for m in config.get('metrics', []):
            if m.get('type') == 'simple':
                self.metrics_receivers.append(SimpleMetrics(m['url']))
            elif m.get('type') == 'carbon':
                self.metrics_receivers.append(CarbonMetrics(m['host'], ident=m.get('id')))

    def send(self, readings):
        for m in self.metrics_receivers:
            #TODO: try-catch?
            m.send(readings.copy())
