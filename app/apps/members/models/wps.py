from django.db import models

from .base import User, UserManager

__all__ = (
    'WPSUserManager',
    'WPSUser',
)


class WPSUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.TYPE_WPS)


class WPSUser(User):
    PERIOD_CHOICES = (
        ('12', '12기'),
    )
    period = models.CharField('기수', choices=PERIOD_CHOICES, max_length=5)

    objects = WPSUserManager()

    def __str__(self):
        return f'{self.name} (WPS, {self.period})기'
