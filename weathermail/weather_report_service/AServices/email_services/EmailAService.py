from weathermail.weather_report_service import email_templates as EmailTemplates

from weathermail.weather_report_service.BServices.email_service.EmailBService import EmailBService


class EmailAService(object):
    """
        Application service designed to do email related operations.
    """

    DEFAULT_SUBJECT = "Enjoy a discount on us!"

    @staticmethod
    def send_weather_report_email(
            state,
            city,
            current_temperature,
            current_weather,
            icon_url,
            discount_url,
            recipient,
            weather_condition=None):
        """
            sending client email based on the current weather condition.

            @type state: str
            @type city: str
            @type current_temperature: float
            @type current_weather: str
            @type icon_url: str
            @type discount_url: str
            @type recipient: str
            @type weather_condition: None or bool
        """

        assert isinstance(state, str), type(state)
        assert isinstance(city, str), type(city)
        assert isinstance(current_temperature, float), type(current_temperature)
        assert isinstance(current_weather, str), type(current_weather)
        assert isinstance(icon_url, str), type(icon_url)
        assert isinstance(discount_url, str), type(discount_url)
        assert isinstance(recipient, str), type(recipient)
        assert weather_condition is None or isinstance(weather_condition, bool), type(weather_condition)

        email_body = {}
        if weather_condition is True:
            email_body['email_message'] = "It's nice out! Enjoy a discount on us."
        elif weather_condition is False:
            email_body['email_message'] = "Not so nice out? That's okay, enjoy a discount on us."
        else:
            email_body['email_message'] = "Enjoy a discount on us."

        email_body['location'] = city + ', ' + state
        email_body['temperature'] = str(current_temperature) + ' F'
        email_body['weather'] = current_weather
        email_body['discount_url'] = discount_url
        email_body['icon_url'] = icon_url

        plaintext_message = EmailTemplates.WeatherEmailText.read() % email_body
        html_template = EmailTemplates.WeatherEmailHTML.read() % email_body

        EmailBService.send_html_message(
            subject=EmailAService.DEFAULT_SUBJECT,
            recipient=recipient,
            plaintext_message=plaintext_message,
            html_message=html_template,
        )
