from rest_framework import serializers
from weathermail.models import PopulousCity, Subscription, MailHistory


class PopulousCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PopulousCity
        fields = ('id', 'name', 'state')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'email', 'city')
