from weathermail.models import Subscription, PopulousCity
from weathermail.serializers import SubscriptionSerializer, PopulousCitySerializer
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status, permissions, renderers
from rest_framework import mixins, generics


# Create your views here.

@permission_classes((permissions.AllowAny,))
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cities': reverse('weathermail:city-list', request=request, format=format)
    })


class SubscriptionList(APIView):
    """
    Create a new Subscription.
    """
    @permission_classes((permissions.IsAuthenticated,))
    def get(self, request, format=None):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, context={'request': request}, many=True)
        return Response(serializer.data)

    @permission_classes((permissions.AllowAny,))
    def post(self, request, format=None):
        serializer = SubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class SubscriptionEmailAvailable(APIView):
    """
    Check if the given email is in use.
    """
    def post(self, request, format=None):
        email = request.data['email']
        if not email:
            return Response("No email specified", status=status.HTTP_400_BAD_REQUEST)
        available = Subscription.objects.filter(email=email).exists() is False
        return Response(available, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class PopulousCityList(APIView):
    """
    Retrieve all cities.
    """
    def get(self, request, format=None):
        cities = PopulousCity.objects.all()
        serializer = PopulousCitySerializer(cities, context={'request': request}, many=True)
        return Response(serializer.data)
