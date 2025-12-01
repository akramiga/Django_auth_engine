from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email if self.email else self.username