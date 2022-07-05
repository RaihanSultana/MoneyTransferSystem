from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Stores a single user entry
    """

    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'


    def __str__(self):
        return "{}".format(self.username) + "-" + str(self.pk)



