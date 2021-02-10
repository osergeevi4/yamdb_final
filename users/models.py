from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    bio = models.CharField(max_length=50,
                           blank=True,
                           verbose_name='Об авторе'
                           )
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Роль'
    )
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
