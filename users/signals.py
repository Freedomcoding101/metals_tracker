from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


def createUserProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        print('created profile')
        profile = Profile.objects.create(
        user=user,
        username=user.username,
        email=user.email,
        name=user.first_name,
        )

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    print('deleted user')
    user.delete()

post_delete.connect(deleteUser, sender=Profile)
post_save.connect(createUserProfile, sender=User)

