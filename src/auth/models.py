from typing import Optional, Any

import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def normalize_email(self, email):
        return email.lower()

    def _create_user(
        self,
        email: str,
        password: str,
        is_staff: bool = False,
        is_superuser: bool = False,
        role: Optional[str] = None
    ) -> 'User':

        email = self.normalize_email(email)
        user: 'User' = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            role=role
        )
        user.set_password(password)
        user.save()

        return user

    def create_user(
            self,
            email: str,
            password: str,
            is_staff: bool = False,
            role: Optional[str] = None
    ) -> 'User':

        return self._create_user(email, password, is_staff=is_staff, role=role)

    def create_superuser(self, email: str, password: str) -> 'User':
        return self._create_user(email, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('merchant', _('Merchant')),
        ('trader', _('Trader')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is staff'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date joined'))

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def profile(self) -> Any:
        match self.role:
            case 'merchant':
                return self.merchant