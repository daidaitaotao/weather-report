from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from weathermail.models import PopulousCity, Subscription

class SubscribeForm(forms.Form):

    # The Form fields
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@email.com'}),
        required=True,
    )
    city = forms.ChoiceField(
        label='Location',
        choices=[[city_model.id, city_model.name + ", " + city_model.state] for city_model in PopulousCity.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Where do you live?'})
    )

    # Custom form validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_in_use = Subscription.objects.filter(email=email).exists()
        if email_in_use:
            raise ValidationError(
                _("We're sorry, but %(email)s is already registered"),
                code='email_in_use',
                params={'email': email},
            )
        return email
