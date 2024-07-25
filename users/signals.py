from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


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

        subject = 'Welcome to Track Stacker'
        message = f'''Dear {user.first_name},

Welcome to Trackstacker! We're thrilled to have you on board and thank you for signing up.

At Trackstacker, we're dedicated to helping you track all your precious metals investments efficiently.

Our software is designed to streamline your management process, providing you with the tools you need to stay on top of your investments effortlessly.

The indexing option will also allow you to label and track your investments for family, ensuring your collection is 

well doccumented and prices and premiums are tracked. Nothing is more important than knowing the value of your investments.

We look forward to supporting you on your journey towards better financial tracking and management.

If you have any questions or need assistance as you get started, please don't hesitate to reach out. Our team is here to help!

Best regards,

Owen Dillabough
Chief Technical Officer,
Trackstacker'''


        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    print('deleted user')
    user.delete()

post_delete.connect(deleteUser, sender=Profile)
post_save.connect(createUserProfile, sender=User)

