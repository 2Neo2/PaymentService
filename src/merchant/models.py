from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class Merchant(models.Model):
    user = models.OneToOneField(
        'custom_auth.User',
        on_delete=models.CASCADE,
        related_name='merchant'
    )

    balance = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=Decimal('0'),
        verbose_name=_('Balance')
    )


class MerchantRegistrationRequest(models.Model):
    email = models.EmailField(verbose_name=_('Email'))
    project_link = models.URLField(verbose_name=_('Project Link'))
    project_description = models.TextField(verbose_name=_('Project Description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', _('Pending')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        ),
        default='pending',
        verbose_name=_('Status')
    )

    class Meta:
        verbose_name = _('Merchant Registration Request')
        verbose_name_plural = _('Merchant Registration Requests')

    def __str__(self):
        return f"{self.email} - {self.get_status_display()}"

    def clean(self):
        super().clean()
        if self.status == 'approved':
            if User.objects.filter(email=self.email).exists():
                raise ValidationError({'email': 'User with this email already exists'})
