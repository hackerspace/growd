import math

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
