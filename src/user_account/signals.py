from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_account.models import UserAccountProfile


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    #   instance.profile.save()
    if created:
        UserAccountProfile.objects.create(user=instance)
    else:
        instance.profile.save()
