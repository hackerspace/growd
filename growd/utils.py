import sys
import math
import logging

def dew_point(temperature, humidity):
    """
    Dew point computation, with error +-0.35C for -45C<=temperature<=60C
    See:
    http://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity/Sensirion_Introduction_to_Relative_Humidity_V2.pdf
    http://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point
    """
    magnus_alpha = 6.112
    magnus_beta = 17.62
    magnus_lambda = 243.12

    gamma = math.log(humidity / 100.0) + ((magnus_beta * temperature) / (magnus_lambda + temperature))
    return (magnus_lambda * gamma) / (magnus_beta - gamma)

def setup_logging(filename=None, verbose=False, timestamp=True):
    format_notime = '%(levelname)-7s %(name)-8s %(message)s'
    format_full = '%(asctime)s ' + format_notime
    fmt = logging.Formatter(
            fmt=(format_full if timestamp else format_notime),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    root = logging.getLogger('')
    root.setLevel(logging.DEBUG)

    log_stderr = logging.StreamHandler(sys.stderr)
    log_stderr.setFormatter(fmt)
    log_stderr.setLevel(logging.DEBUG if verbose else logging.INFO)
    root.addHandler(log_stderr)

    requests = logging.getLogger('requests')
    requests.setLevel(logging.WARNING)

    if filename:
        fmt = logging.Formatter(
                fmt=format_full,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        log_file = logging.FileHandler(filename=filename)
        log_file.setFormatter(fmt)
        log_file.setLevel(logging.DEBUG)
        root.addHandler(log_file)
