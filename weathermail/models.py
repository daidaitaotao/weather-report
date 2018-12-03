from django.db import models

# Create your models here.

class PopulousCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    class Meta:
        ordering = ('name',)


class Subscription(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey(PopulousCity, on_delete=models.PROTECT)

    class Meta:
        ordering = ('created',)


class MailHistory(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    lastsent = models.DateTimeField('date last sent')
    wassuccessful = models.BooleanField(default=False)

    class Meta:
        ordering = ('lastsent',)

class WeatherHistory(models.Model):
    city = models.ForeignKey(PopulousCity, on_delete=models.PROTECT, null=False)
    history_date = models.DateTimeField('history date', null=False)
    temperature = models.FloatField('history temperature', null=False)
    weather = models.CharField(max_length=100, null=True)
    icon_url = models.URLField(null=True)

    class Meta:
        ordering = ('history_date',)
