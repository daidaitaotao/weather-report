import logging
from datetime import datetime, timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand

from weathermail.models import Subscription, MailHistory, PopulousCity
from weathermail.weather_report_service.AServices.weather_report.WeatherReportAService import WeatherReportAService
from weathermail.weather_report_service.AServices.email_services.EmailAService import EmailAService

class Command(BaseCommand):
    help = 'Process all users subscribed to weathermail and send each a weather-related email, if they have not been sent one in the past 24 hours.'

    def handle(self, *args, **options):
        all_subs = Subscription.objects.all()
        one_day_ago = timezone.now().today() - timedelta(days=1)
        email_list = {}
        for sub in all_subs:
            self.stdout.write(self.style.SUCCESS('Processing subscription for {0} in {1}'.format(sub.email, sub.city.name)))

            # Check if the subscription has already been sent an email within the past 24 hours
            last_sent_history = MailHistory.objects.filter(subscription=sub).filter(wassuccessful=True).filter(lastsent__gt=one_day_ago).first()
            if last_sent_history:
                continue

            city_name = (sub.city.name + '_' + sub.city.state).replace(' ', '_')
            if city_name not in email_list:
                email_list['city_name'] = {
                    'city_entity': sub.city,
                    'emails': [sub.email]
                }
            else:
                email_list['city_name']['email'].append(sub.email)

        # send emails group by location
        for key, value in email_list.items():
            successful = True
            try:
                city_location = value['city_entity']
                emails = value['emails']

                # getting weather condition
                (current_temperature_f,
                weather,
                icon_url,
                discount_url,
                weather_condition,) = WeatherReportAService.get_weather_report_compared_history(
                    city_location
                )
            except Exception as e:
                successful = False
                # maybe log error
                Command.__LOGGER.error('error when getting weather information from %s, %s, %s',
                                       sub.city.name,
                                       sub.city.state,
                                       e)
            if successful:
                for email in emails:
                    sent = True
                    try:
                        EmailAService.send_weather_report_email(
                            city_location.state,
                            city_location.name,
                            current_temperature_f,
                            weather,
                            icon_url,
                            discount_url=discount_url,
                            recipient=email,
                            weather_condition=weather_condition,
                        )
                        self.stdout.write(self.style.SUCCESS('Sent out email for %s' % sub.email))
                    except Exception as e:
                        sent = False
                        # maybe log error
                        Command.__LOGGER.error('error when send out email to %s, %s', sub.email, e)

                    # Record whether the email was send successfully and when
                    new_history = MailHistory(lastsent=timezone.now(), wassuccessful=sent, subscription=sub)
                    new_history.save()

        self.stdout.write(self.style.SUCCESS('Successfully processed %s subscriptions' % all_subs.count()))

    __LOGGER = logging.getLogger(__name__)
    """ logger for current class """
