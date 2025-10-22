import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(AbstractUser):
    """
    Модель пользователя.
    """
    id = models.UUIDField(
        'Идентификатор пользователя',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        'Ник пользователя',
        max_length=256,
        blank=True,
        null=True,
        unique=False
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        validators=[EmailValidator()]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Пользователь {self.username}'


class Profile(models.Model):
    """
    Модель профиля пользователя.
    """
    user = models.OneToOneField(
        Customer, on_delete=models.CASCADE
    )
    first_name = models.CharField(
        'Имя',
        max_length=256,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=256,
        blank=True,
        null=True
    )
    bio = models.TextField(
        'Краткая биография',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Пользователь {self.user.username}'


@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Customer)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
