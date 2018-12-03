from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from weathermail import apiviews, views

app_name='weathermail'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/$', apiviews.api_root),
    url(r'^api/city/$', apiviews.PopulousCityList.as_view(), name='city-list'),
    url(r'^api/sub/$', apiviews.SubscriptionList.as_view(), name='sub-list'),
    url(r'^api/sub/available$', apiviews.SubscriptionEmailAvailable.as_view(), name='email-available'),
]

# Allow for the format of the API response to be determined by a file extension.
# For example, http://localhost:8000/snippets/4.json will return a JSON response.
urlpatterns = format_suffix_patterns(urlpatterns)