from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser

from api.constants import CONFIRMATION_CODE_LENGTH

ROLES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь')
)


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == (
            'admin' or self.is_superuser or self.is_staff
        )


class Category(models.Model):
    """Класс категорий."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Cлаг',
        max_length=50,
        unique=True,
        validators=[validators.RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг содержит недопустимые символы'
        )]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self) -> str:
        return self.name
