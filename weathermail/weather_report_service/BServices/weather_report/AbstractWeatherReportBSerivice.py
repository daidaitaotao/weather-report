from urllib.request import urlopen
import requests
import json
import time
from weathermail.config.weather_app import weather_app


class AbstractWeatherReportBService(object):
    """
        Abstract BService layer for Weather Report
    """

    METHOD_CONDITION = 'conditions'

    METHOD_FORECAST = 'forecast'

    METHOD_HISTORY = 'history_'

    @staticmethod
    def get_wunder_condition_json_response(
            state,
            city,
            retry_attempts=None,
            retry_delay=None,
    ):
        """
            calling the wunder api to obtain current weather report in json format

            @type city: str
            @type state: str
            @type retry_attemps: int
            @type retry_delay: int

            @rtype: json
        """
        assert isinstance(state, str), type(state)
        assert isinstance(city, str), type(city)
        assert retry_attempts is None or isinstance(retry_attempts, int), type(retry_attempts)
        assert retry_delay is None or isinstance(retry_delay, int), type(retry_delay)

        request_url = '/'.join([AbstractWeatherReportBService.__BASE_API,
                       weather_app.WEATHER_PRIVATE_KEY,
                       AbstractWeatherReportBService.METHOD_CONDITION,
                       'q',
                       state,
                       city])
        request_url = request_url + AbstractWeatherReportBService.__OUTPUT_FORMAT

        if not retry_attempts:
            return AbstractWeatherReportBService._making_api_request(request_url)
        else:
            # here we try to do retry flow manually so we may have better handling for the response
            response = None
            tries = 0
            while tries < retry_attempts:
                try:
                    response = requests.get(request_url)
                except Exception as e:
                    if tries == retry_attempts - 1:
                        raise e
                    else:
                        continue
                if response.status_code != 200:
                    tries += 1
                    if retry_delay:
                        time.sleep(retry_delay)
                    continue
                else:
                    return response.json()
            # if the function gets here, we know the api call did not success
            raise Exception('unable to get valid response %s', response.status_code)

    @staticmethod
    def get_wunder_history_json_response(
            state,
            city,
            date_string,
            retry_attempts=None,
            retry_delay=None,
    ):
        """
            obtain weather history by given city, state and date in YYYMMDD format

            @type city: str
            @type state: str
            @type date_string: str
            @type retry_attempts: int
            @type retry_delay: int

            @rtype: json
        """
        assert isinstance(state, str), type(state)
        assert isinstance(city, str), type(city)
        assert isinstance(date_string, str), type(date_string)
        assert retry_attempts is None or isinstance(retry_attempts, int), type(retry_attempts)
        assert retry_delay is None or isinstance(retry_delay, int), type(retry_delay)

        request_url = '/'.join([AbstractWeatherReportBService.__BASE_API,
                       weather_app.WEATHER_PRIVATE_KEY,
                       AbstractWeatherReportBService.METHOD_HISTORY + date_string,
                       'q',
                       state,
                       city]) + AbstractWeatherReportBService.__OUTPUT_FORMAT

        if not retry_attempts:
            return AbstractWeatherReportBService._making_api_request(request_url)
        else:
            response = None
            tries = 0
            # here we try to do retry flow manually so we may have better handling for the response
            while tries < retry_attempts:
                try:
                    response = requests.get(request_url)
                except Exception as e:
                    if tries == retry_attempts - 1:
                        raise e
                    else:
                        continue
                if response.status_code != 200:
                    tries += 1
                    if retry_delay:
                        time.sleep(retry_delay)
                    continue
                else:
                    return response.json()
            # if the function gets here, we know the api call did not success
            raise Exception('unable to get valid response %s', response.status_code)

    @staticmethod
    def _making_api_request(request_url):
        assert isinstance(request_url, str), type(request_url)
        r = requests.get(request_url)
        parsed_json = r.json()
        return parsed_json

    __BASE_API = 'http://api.wunderground.com/api'

    __OUTPUT_FORMAT = '.json'

