from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, User)
from django.db import models


class UserAccountManager(BaseUserManager):

    def create_user(self, email, name, person_telephone, surname, password=None):

        if not email:
            raise ValueError("Почта должна быть указана")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, person_telephone=person_telephone, surname=surname)

        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, email, name, person_telephone, surname, password=None):

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, person_telephone=person_telephone, surname=surname)
        user.set_password(password)
        user.save()

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),

)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')
    person_rating = models.IntegerField('Рейтинг клиента', blank=True, null=True)
    person_created = models.DateTimeField('Дата создания аккаунта', auto_now=True)
    person_telephone = models.CharField('Номер телефона', max_length=20, blank=True)
    person_address = models.CharField('Адрес', max_length=200, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'person_telephone', 'surname']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

