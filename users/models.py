"""Users models."""

# Django
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class Profile(models.Model):
    """Profile model.

    Proxy model that extends the base data with other
    information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username


@receiver(user_signed_up)
def create_user_profile(request, user, **kwargs):
    """ Create user profile when sign up with Facebook """

    profile = Profile.objects.create(user=user)
    profile.save()
