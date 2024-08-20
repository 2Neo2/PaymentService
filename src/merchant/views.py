from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import MerchantRegistrationRequest
from .forms import MerchantRegistrationForm, MerchantLoginForm
from auth.models import User


class MerchantRegistrationView(CreateView):
    model = MerchantRegistrationRequest
    form_class = MerchantRegistrationForm
    template_name = 'merchant/merchant_registration.html'
    success_url = reverse_lazy('merchant:registration_success')


class RegistrationSuccessView(TemplateView):
    template_name = 'merchant/registration_success.html'


class RegistrationLoginView(CreateView):
    model = User
    form_class = MerchantLoginForm
    template_name = 'merchant/login.html'


class MerchantDashboardView(TemplateView):
    template_name = 'merchant/dashboard.html'
