from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(
        max_length = 20,
        unique = True,
        null = False,
    )
    email = models.EmailField(
        max_length = 40,
        unique = True,
        null = False
    )
    password = models.CharField(
        max_length = 128,
        null = False,
    )
    first_name = models.CharField(
        max_length = 20,
        null = False,
    )
    last_name = models.CharField(
        max_length = 20,
        null = False,
    )
    is_verification = models.BooleanField(
        default = False,
        null = False,
    )
    pay_id = models.CharField(
        max_length = 50,
        null = False,
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
    
    

