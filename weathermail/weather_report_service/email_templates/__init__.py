import codecs
import os

path = os.path.dirname(os.path.abspath(__file__))

WeatherEmailHTML = codecs.open('{0}/weather_email.html'.format(path), 'r')
WeatherEmailText = codecs.open('{0}/weather_email.txt'.format(path), 'r')