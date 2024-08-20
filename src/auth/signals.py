from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User
from merchant.models import Merchant


@receiver(post_save, sender=User, weak=False)
def create_profile(sender: object, instance: User, created: bool, **kwargs) -> None:
    if created:
        match instance.role:
            case 'merchant':
                Merchant.objects.create(user=instance)
