from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator

import random


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_COICES = [
        ('guest', 'Гость'),
        ('expert', 'Эксперт'),
    ]
        
    id = models.BigIntegerField(primary_key=True, unique=True, editable=False,)
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_COICES, default='guest')
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_groups',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        """Генерирует уникальный 7-значный ID для пользователя"""
        max_attempts = 100  # увеличиваем количество попыток
        for _ in range(max_attempts):
            new_id = random.randint(1000000, 9999999)
            # Используем прямой импорт модели для избежания циклических зависимостей
            from django.apps import apps
            User = apps.get_model('user', 'User')
            if not User.objects.filter(id=new_id).exists():
                return new_id
        raise ValueError("Не удалось сгенерировать уникальный ID пользователя после {} попыток".format(max_attempts))
