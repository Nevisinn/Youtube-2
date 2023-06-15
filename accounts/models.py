from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Ваш email адресс', unique=True,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email_verify = models.BooleanField(default=False)

