from enum import StrEnum

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import UserManager


class UserRoles(StrEnum):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractBaseUser):
    ROLE = [
        (UserRoles.USER, "Пользователь"),
        (UserRoles.ADMIN, "Администратор"),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64, default='')
    last_name = models.CharField(max_length=64, default='')
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    role = models.CharField(max_length=5, choices=ROLE, default="user")
    image = models.ImageField(blank=True, null=True, upload_to="user_pic/")
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    # Необходимые параметры для корректной работе Django
    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    # также для работы модели пользователя должен быть переопределен
    # менеджер объектов
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
