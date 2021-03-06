from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser, UserManager)
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone
from datetime import datetime, timedelta
import jwt

from django.conf import settings

class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email) 
        username = self.model.normalize_username(username)  

        user = self.model(
            username = username,
            email = email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('email_verified', False)
        extra_fields.setdefault('date_joined', datetime.now())
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_supperuser = True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    is_active = models.BooleanField(blank=True)
    date_joined = models.DateTimeField(blank=True)
    email_verified = models.BooleanField(blank=True)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'   
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        token = jwt.encode(
            {'username': self.username, 'email': self.email,
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')

        return token

