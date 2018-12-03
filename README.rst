=====
weathermail
=====

Weathermail is a Django app that allows users to enter their email address, select the
closest large US city to them, and subscribe to get weather-based emails.  A service
is included that will send out one email per day to each subscriber whose body is
determined by the current day's forcast.

This is version 0.1.1 of this app.

Quick start
-----------

1. Check the requirements for this app in requirement.txt in 'weather_app/requirements.txt' `pip freeze > requirements.txt`
    If you wish to install all required libraries, simply run 'pip install -r requirements.txt'

2. Add "weathermail" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'rest_framework',
        'weathermail.apps.WeathermailConfig'
    ]

3. Include the weathermail URLconf in your project urls.py like this::

    url(r'^wm/', include('weathermail.urls'))

4. Go to /config/weather_app.py to insert an API key which to retrieve weather data, you can register the key at:
    https://www.wunderground.com/weather/api/

5. Run 'python manage.py migrate' to create the weathermail models.

6. Run 'python manage.py loaddata populous_cities.json' to insert all city and state data into database.

7. Go to the front page http://localhost:8000/wm/ to enter a valid email address and select a location, and then click subscribe button.

7. Run 'python manage.py sendweathermail' An email should be sent to the address you just put in step 5.