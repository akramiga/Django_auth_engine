from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # add extra fields later if needed
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username or self.email