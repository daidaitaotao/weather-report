from __future__ import absolute_import

import datetime
import logging
from pytz import timezone

from weathermail.models import WeatherHistory
from weathermail.weather_report_service.BServices.weather_report.AbstractWeatherReportBSerivice import \
    AbstractWeatherReportBService


class WeatherReportBService(AbstractWeatherReportBService):
    """
        Business layer insight service for transformation between Wordstream VOs and
        Facebook objects.
    """

    @staticmethod
    def get_current_weather(
            state,
            city,
            retry_attempts=None,
            retry_delay=None
    ):
        """
            retrieve current weather by given state and city

            @type state: str
            @type city: str
            @type retry_attempts: int
            @type retry_delay: int

            @rtype: dict
        """
        assert isinstance(state, str), type(state)
        assert isinstance(city, str), type(city)

        try:
            current_weather = WeatherReportBService.get_wunder_condition_json_response(
                state,
                city,
                retry_attempts=retry_attempts,
                retry_delay=retry_delay,
            )
        except Exception as e:
            WeatherReportBService.__LOGGER.error(
                'unable to get current weather for %s, %s becase: %s',
                state,
                city,
                e
            )
            raise

        return current_weather

    @staticmethod
    def get_history_temperature_detailed_in_hour_f(
            state,
            city,
            date_time_detail,
            retry_attempts=None,
            retry_delay=None
    ):
        """
            getting history temperature based on giving date and the result will detailed in given
            date'hour.

            @type state: str
            @type city: str
            @type date_time_detail: datetime.datetime
            @type retry_attempts: int
            @type retry_delay: int

            rtype: float
        """
        assert isinstance(state, str), type(state)
        assert isinstance(city, str), type(city)
        assert isinstance(date_time_detail, datetime.datetime), type(date_time_detail)
        assert isinstance(retry_attempts, int), type(retry_attempts)
        assert isinstance(retry_delay, int), type(retry_delay)

        # convert date_time to utc
        if date_time_detail.tzinfo is not None and date_time_detail.tzinfo.utcoffset(date_time_detail) is not None:
            utc_datetime = date_time_detail.astimezone(timezone('UTC'))
        else:
            utc_datetime = date_time_detail
        hour = utc_datetime.hour
        date_string = utc_datetime.strftime('%Y%m%d')
        try:
            history_weather = WeatherReportBService.get_wunder_history_json_response(
                state,
                city,
                date_string,
                retry_attempts=retry_attempts,
                retry_delay=retry_delay,
            )
        except Exception as e:
            WeatherReportBService.__LOGGER.error(
                'unable to get history weather for %s, %s becase: %s',
                state,
                city,
                e
            )
            raise

        most_closed_temperature_f = None
        max_hour_diff = 24
        if 'history' in history_weather and 'observations' in history_weather['history']:
            hourly_observations = history_weather['history']['observations']
            for observation in hourly_observations:
                if 'utcdate' in observation and 'hour' in observation['utcdate']:
                    history_hour = int(observation['utcdate']['hour'])
                    hour_diff = abs(hour - history_hour)
                    if max_hour_diff >= hour_diff:
                        most_closed_temperature_f = float(observation['tempi'])
                else:
                    continue

        return most_closed_temperature_f

    @staticmethod
    def get_current_weather_data(city_location, current_date):
        """
            getting current weather from database or API response based on giving date and the result will detailed in
            given date'hour.

            @type city_location: PopulousCity
            @type current_date: datetime.datetime

            rtype: tuple
        """
        current_weather_entity = WeatherHistory.objects.filter(city=city_location).filter(history_date=current_date).first()
        if current_weather_entity and current_weather_entity.weather and current_weather_entity.icon_url:
            current_temperature_f = current_weather_entity.temperature
            weather = current_weather_entity.weather
            icon_url = current_weather_entity.icon_url
        else:
            city = city_location.name
            state = city_location.state

            if ' ' in city:
                city = city.replace(' ', '_')
            current_weather = WeatherReportBService.get_current_weather(
                state,
                city,
            )
            current_observation = current_weather['current_observation']
            current_temperature_f = float(current_observation['temp_f'])
            weather = current_observation['weather']
            icon_url = current_observation['icon_url']
            if current_weather_entity:
                current_weather_entity.temperature = current_temperature_f
                current_weather_entity.weather = weather
                current_weather_entity.icon_url = icon_url
                current_weather_entity.save()
            else:
                new_weather = WeatherHistory(
                    city=city_location,
                    history_date=current_date,
                    temperature=current_temperature_f,
                    weather=weather,
                    icon_url=icon_url,
                )
                new_weather.save()
        return (current_temperature_f, weather, icon_url,)

    @staticmethod
    def get_history_temperature_data(city_location, history_date):
        """
            getting history weather temperature from database or API response based on giving date and the result will
            detailed in given date'hour.

            @type city_location: PopulousCity
            @type current_date: datetime.datetime

            rtype: float
        """
        history_temperature = None
        history_weather_entity = WeatherHistory.objects.filter(
            city=city_location).filter(history_date=history_date).first()
        if history_weather_entity:
            history_temperature = history_weather_entity.temperature
        else:
            city = city_location.name
            state = city_location.state
            if ' ' in city:
                city = city.replace(' ', '_')
            history_weather_temperature = WeatherReportBService.get_history_temperature_detailed_in_hour_f(
                state,
                city,
                history_date,
                retry_attempts=WeatherReportBService.__RETRY_ATTEMPTS,
                retry_delay=WeatherReportBService.__RETRY_DELAY,
            )
            history_weather_entity = WeatherHistory(city=city_location, history_date=history_date,
                                                    temperature=history_weather_temperature)
            history_weather_entity.save()
            history_temperature = history_weather_temperature
        return history_temperature

    __RETRY_ATTEMPTS = 5
    """ number of retries for the api call """

    __RETRY_DELAY = 2
    """ amount of delay before retrying in seconds """

    __DATE_FORMAT = '%Y%m%d'
    """ date format for history """

    __LOGGER = logging.getLogger(__name__)
    """ logger for current class """

