from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email
from .models import MerchantRegistrationRequest
from auth.models import User


class MerchantRegistrationForm(forms.ModelForm):
    class Meta:
        model = MerchantRegistrationRequest
        fields = ['email', 'project_link', 'project_description']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'project_link': forms.URLInput(attrs={'class': 'form-control'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        value = self.cleaned_data['email']

        try:
            validate_email(value)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

        return value.lower()

    def clean_project_link(self):
        value = self.cleaned_data['project_link']

        validate_url = URLValidator()
        try:
            validate_url(value)
        except ValidationError:
            raise forms.ValidationError("Enter a valid URL.")

        return value.lower()


class MerchantLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
