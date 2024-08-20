import random
import string

from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django import forms

from .models import MerchantRegistrationRequest
from auth.models import User


class MerchantRegistrationAdminForm(forms.ModelForm):
    class Meta:
        model = MerchantRegistrationRequest
        fields = ['email', 'project_link', 'project_description', 'status']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        status = cleaned_data.get('status')

        if status == 'approved':
            if User.objects.filter(email=email).exists():
                self.add_error('email', 'User with this email already exists.')

        return cleaned_data


@admin.register(MerchantRegistrationRequest)
class MerchantRegistrationRequestAdmin(admin.ModelAdmin):
    form = MerchantRegistrationAdminForm  # Привязка кастомной формы
    list_display = ('email', 'status', 'created_at')
    search_fields = ('email',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    fieldsets = [
        (
            'Информация по заявке',
            {
                "fields": ["email", "project_link", "project_description"],
            },
        ),
        (
            'Дата создания',
            {
                "fields": ["created_at"],
            },
        ),
        (
            'Статус',
            {
                "fields": ["status"],
            },
        ),
    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['email', 'created_at', 'project_link', 'project_description']
        if obj and obj.status != 'pending':
            readonly_fields.append('status')
        return readonly_fields

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def save_model(self, request, obj, form, change):
        if obj.status == 'approved':
            login_link = "http://127.0.0.1:8000/merchant/login"
            password = self.generate_random_password()

            User.objects.create_user(
                email=obj.email,
                password=password,
                is_staff=False,
                role='merchant'
            )

            send_mail(
                'Ваша заявка одобрена!',
                f'Здравствуйте, ваша заявка была одобрена.\nПерейдите по ссылке для входа: {login_link}\n'
                f'Ваш пароль: {password}',
                settings.EMAIL_HOST_USER,
                [obj.email],
                fail_silently=False,
            )

        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_staff', 'date_joined')
    ordering = ('-date_joined',)
    readonly_fields = ('id', 'email', 'date_joined')
    fieldsets = [
        (
            'Информация о пользователе',
            {
                "fields": ["id", "email", "is_staff", "is_active"],
            },
        ),
        (
            'Дата создания аккаунта',
            {
                "fields": ["date_joined"],
            },
        ),
    ]


