from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.MerchantRegistrationView.as_view(), name='merchant_registration'),
    path('register/success/', views.RegistrationSuccessView.as_view(), name='registration_success'),
    path('login/', views.RegistrationLoginView.as_view(), name='merchant_login'),
    path('dashboard/', views.MerchantDashboardView.as_view(), name='merchant_dashboard')
]
