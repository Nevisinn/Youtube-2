from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Ваш email адресс', unique=True,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email_verify = models.BooleanField(default=False)
    subscribers_count = models.PositiveIntegerField(default=0)


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    channel_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ['subscriber', 'channel_user']


