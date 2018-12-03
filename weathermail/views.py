from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic, View
from django.urls import reverse
from django.core import mail
from weathermail.models import PopulousCity, Subscription
from weathermail.forms import SubscribeForm

# Create your views here.

class IndexView(View):
    template_name = 'weathermail/index.html'

    def get(self, request, *args, **kwargs):
        form = SubscribeForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, { 'form': form })

        email = form.cleaned_data['email']
        city_pk = form.cleaned_data['city']
        print(form.cleaned_data)

        city = PopulousCity.objects.get(pk=city_pk)
        sub = Subscription(email=email, city=city)
        sub.save()

        return render(request, self.template_name, {
            'form': form,
            'success_message': "Congratulation! You have successfully registered " + email + " for exiting new emails.",
        })
