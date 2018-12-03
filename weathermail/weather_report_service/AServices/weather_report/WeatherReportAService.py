import datetime
import logging
from django.utils import timezone
from weathermail.weather_report_service.BServices.weather_report.WeatherReportBService import WeatherReportBService

from weathermail.weather_report_service.utils.DateUtils import DateUtils


class WeatherReportAService(object):
    """
        Application service designed to do weather report related operations.
    """

    DEFAULT_DISCOUNT_URL = 'https://www.weathermail.com'

    @staticmethod
    def get_weather_report_compared_history(city_location):
        """
            getting the current weather report for given city and state and compares it to the previous average weather
            , and send email to client based on the comparision result.

            @type: state: str
        """
        assert isinstance(city_location.name, str), type(city_location.name)
        assert isinstance(city_location.state, str), type(city_location.state)
        assert city_location.name
        assert city_location.state

        current_date = timezone.now().replace(minute=0, second=0, microsecond=0)
        (current_temperature_f,
         weather,
         icon_url,) = WeatherReportBService.get_current_weather_data(
            city_location,
            current_date,
        )
        weather_condition = None
        if 'sunny' in weather.lower():
            return (current_temperature_f,
                    weather,
                    icon_url,
                    WeatherReportAService.DEFAULT_DISCOUNT_URL,
                    weather_condition,)
        else:
            date_last_year = DateUtils.get_same_day_n_year_ago(current_date, 1)
            date_last_2_years = DateUtils.get_same_day_n_year_ago(current_date, 2)
            date_last_3_years = DateUtils.get_same_day_n_year_ago(current_date, 3)

            temperature_f_last_year = WeatherReportBService.get_history_temperature_data(
                city_location,
                date_last_year
            )
            temperature_f_last_2_years = WeatherReportBService.get_history_temperature_data(
                city_location,
                date_last_2_years,
            )
            temperature_f_last_3_years = WeatherReportBService.get_history_temperature_data(
                city_location,
                date_last_3_years,
            )
            average_temperature_f = (temperature_f_last_year +
                                     temperature_f_last_2_years +
                                     temperature_f_last_3_years) / 3
            if current_temperature_f - average_temperature_f >= WeatherReportAService.__GOOD_WEATHER_TEMP:
                weather_condition = True
            elif current_temperature_f - average_temperature_f <= WeatherReportAService.__BAD_WEATHER_TEMP:
                weather_condition = False
            else:
                weather_condition = None

            return (current_temperature_f,
                    weather,
                    icon_url,
                    WeatherReportAService.DEFAULT_DISCOUNT_URL,
                    weather_condition,)

    __GOOD_WEATHER_TEMP = 5
    """ good weather temperature diff compared to average history temperature """

    __BAD_WEATHER_TEMP = -5
    """ bad weather temperature diff compared to average history temperature """
    __LOGGER = logging.getLogger(__name__)
    """ logger for the current class """
